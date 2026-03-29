from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from datetime import timedelta
from database import get_db
from models.auth import User
from fastapi.security import OAuth2PasswordRequestForm 
from models.schemas import UserCreate, UserResponse, UserUpdate
from core.security import create_access_token, hash_password, verify_password, get_current_user
from core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    db_user = User(
        full_name=user.full_name,
        email=user.email,
        hashed_password=hash_password(user.password),
        role=user.role,
        phone_number=user.phone_number,
        date_of_birth=user.date_of_birth,
        gender=user.gender,
        address=user.address,
        emergency_contact_name=user.emergency_contact_name,
        emergency_contact_phone=user.emergency_contact_phone
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is inactive")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": str(user.id)}, expires_delta=access_token_expires)
    
    return {"access_token": access_token, "token_type": "bearer", "user": UserResponse.from_orm(user)}

@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserResponse)
def update_profile(profile_update: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    update_data = profile_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/upload-profile-picture")
def upload_profile_picture(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    import os
    from core.config import settings
    
    if not os.path.exists(settings.UPLOAD_DIR):
        os.makedirs(settings.UPLOAD_DIR)
    
    file_path = f"{settings.UPLOAD_DIR}/{current_user.id}_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    
    user = db.query(User).filter(User.id == current_user.id).first()
    user.profile_picture_url = file_path
    db.add(user)
    db.commit()
    
    return {"filename": file.filename, "profile_picture_url": file_path}