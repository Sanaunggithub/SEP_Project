from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import sys
import os

# Add backend directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import engine
from models.base import Base

# Import ALL your models so alembic can detect them
from models.auth import User
from models.student import Student
from models.course import Course, CourseEnrollment
from models.grade import Grade
from models.attendance import Attendance
from models.assignment import Assignment, Submission
from models.notification import Notification
from models.analytics import ReportSnapshot

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ← this was None before, that's the problem
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    from core.config import settings
    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    from core.config import settings
    from sqlalchemy import create_engine
    
    connectable = create_engine(settings.DATABASE_URL)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()