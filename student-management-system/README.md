# Student Management System

## Overview
A comprehensive role-based student management system with separate admin and student interfaces. The application provides tools for managing students, courses, grades, attendance, assignments, and analytics. Built with PyScript frontend and FastAPI backend.

## Features

### Admin Features
- **Student Management**: Add, edit, and manage student records
- **Course Management**: Create and manage courses
- **Grade Management**: Track and update student grades
- **Attendance Tracking**: Monitor student attendance records
- **Assignment Management**: Create and track assignments
- **Analytics Dashboard**: View system-wide statistics and insights
- **Admin Dashboard**: Central hub with navigation to all management functions

### Student Features
- **Dashboard**: Overview of courses, grades, and recent activities
- **My Courses**: View enrolled courses with progress tracking
- **My Grades**: Track grades across all courses with color-coded status badges
- **My Attendance**: View attendance records and statistics
- **My Assignments**: Track assignment status (pending, completed, overdue)

### Core Features
- **Role-Based Authentication**: Separate login for admin and student users
- **PyScript Integration**: Frontend Python execution for interactive UI
- **Responsive Design**: Bootstrap 5 for mobile and desktop compatibility
- **Secure Session Management**: localStorage-based authentication with tokens

## Project Structure
```
student-management-system
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── database.py             # Database configuration
│   ├── models/                 # Data models
│   ├── routers/                # API endpoint routers
│   └── schemas/                # Request/response schemas
├── frontend/
│   ├── pages/
│   │   ├── login.html         # Authentication page
│   │   ├── admin/             # Admin pages
│   │   │   ├── dashboard.html
│   │   │   ├── student.html
│   │   │   ├── course.html
│   │   │   ├── grade.html
│   │   │   ├── attendance.html
│   │   │   ├── assignment.html
│   │   │   └── analytics.html
│   │   └── student/           # Student pages
│   │       ├── dashboard.html
│   │       ├── my-courses.html
│   │       ├── my-grades.html
│   │       ├── my-attendance.html
│   │       └── my-assignments.html
│   ├── index.html             # Admin landing page
│   ├── style.css
│   ├── components/
│   ├── scripts/
│   └── pages/
├── src/                        # Legacy components (being integrated)
├── requirements.txt
└── README.md
```

## Tech Stack
- **Frontend**: 
  - PyScript 2024.1.1 (Python execution in browser)
  - Bootstrap 5.3.0 (Responsive UI framework)
  - Bootstrap Icons 1.11.0 (Icon library)
  - Chart.js 3.9.1 (Data visualization)
- **Backend**: FastAPI, Python
- **Database**: SQLAlchemy ORM (configured, pending migration)
- **Authentication**: Token-based with localStorage
- **Version Control**: Git

## Installation

### Prerequisites
- Python 3.8+
- Node.js (optional, for any frontend tooling)

### Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd student-management-system
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up backend (optional - for API integration):
   ```bash
   cd backend
   pip install -r ../requirements.txt
   uvicorn main:app --reload --port 8000
   ```
   The backend API will be available at `http://localhost:8000`

## Usage

### Starting the Application

#### For Admin Users:
1. Open `frontend/index.html` in a web browser
2. Log in with admin credentials
3. Access the admin dashboard with links to:
   - Student Management
   - Course Management
   - Grade Tracking
   - Attendance Records
   - Assignment Management
   - Analytics Dashboard

#### For Student Users:
1. Open `frontend/pages/login.html` in a web browser
2. Log in with student credentials
3. Access your student dashboard with links to:
   - My Courses (with progress tracking)
   - My Grades (with GPA calculation)
   - My Attendance (with attendance rate)
   - My Assignments (with status tracking)

### Default Test Credentials

**Admin User:**
- Email: admin@example.com
- Password: admin123

**Student User:**
- Email: student@example.com
- Password: student123

### Admin Navigation Flow
Admin Dashboard → Student/Course/Grade/Attendance/Assignment Management → Analytics Dashboard

## Design & Architecture

### UI Framework
- **Responsive Layout**: Two-column design with sticky sidebar navigation
- **Color Scheme**: 
  - Primary Gradient: Purple (#667eea) to Violet (#764ba2)
  - Success: Green (#10b981) - for present/completed
  - Warning: Yellow (#f59e0b) - for pending
  - Danger: Red (#ef4444) - for failed/absent
- **Typography**: Segoe UI with semantic font scaling
- **Components**: Bootstrap grid system for responsive design

### Frontend Architecture
- **CSS Variables**: `:root` variables for consistent theming across pages
- **PyScript Classes**: Object-oriented page logic with methods for auth, data setup, rendering, and event handling
- **Sample Data**: JavaScript arrays for testing without backend connection
- **Event Listeners**: Dynamic interactivity for search, filters, and navigation

### Authentication Flow
1. User visits login.html
2. Frontend checks localStorage for token
3. On login, token and role stored in localStorage
4. Role-based redirect to appropriate dashboard
5. All pages verify token and role before rendering
6. Logout clears localStorage and redirects to login

## Current Status
- ✅ **Frontend - Admin Pages**: Complete with full CRUD interfaces
  - Dashboard with quick stats and actions
  - Student Management
  - Course Management
  - Grade Management
  - Attendance Tracking
  - Assignment Management
  - Analytics Dashboard with Chart.js visualizations
- ✅ **Frontend - Student Pages**: Complete with read-only interfaces
  - Student Dashboard with statistics
  - My Courses with search and progress tracking
  - My Grades with GPA calculation
  - My Attendance with attendance statistics
  - My Assignments with status tracking
- ✅ **Role-Based Authentication**: Login system with localStorage tokens
- ✅ **Responsive Design**: Bootstrap 5 mobile-friendly layouts
- ⏳ **Backend**: FastAPI endpoints (in development)
- ⏳ **Database**: SQLAlchemy models configured (migrations pending)
- ⏳ **API Integration**: Frontend-backend connection (pending)

## Future Enhancements
- Backend API integration with all frontend pages
- Database implementation with migration scripts
- Advanced analytics and reporting features
- File upload functionality for documents and avatars
- Email notifications for assignment deadlines
- Student search and filtering in admin panel
- Grade statistics and performance insights per course
- Real-time attendance tracking via QR code

## Troubleshooting

### Issue: Pages not loading or showing blank
- **Solution**: Ensure you have JavaScript enabled and allow PyScript to load from CDN
- **Check**: Browser console for errors (F12 → Console tab)

### Issue: Authentication redirects to login repeatedly
- **Solution**: Clear browser localStorage (F12 → Application → Local Storage → Clear)
- **Ensure**: Using correct test credentials or logging in first

### Issue: Charts not showing in Analytics Dashboard
- **Solution**: Ensure Chart.js CDN is accessible and browser allows external scripts
- **Refresh**: Hard refresh the page (Ctrl+Shift+R or Cmd+Shift+R)

### Issue: Sidebar not displaying correctly on mobile
- **Solution**: Use responsive design breakpoint - sidebar collapses on screens < 768px
- **Test**: Use browser developer tools to test mobile view

## Contributing
1. Create a new branch for your feature
2. Make your changes
3. Test thoroughly on different screen sizes
4. Submit a pull request with clear description

## Project Authors
Student Management System Development Team

## License
MIT License