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
│   │   │   ├── notification.html
│   │   │   └── analytics.html
│   │   └── student/           # Student pages
│   │       ├── dashboard.html
│   │       ├── my-courses.html
│   │       ├── my-grades.html
│   │       ├── my-attendance.html
│   │       ├── my-assignments.html
│   │       └── notifications.html
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
- **Frontend**: PyScript 2024.1.1, Bootstrap 5.3.0, Bootstrap Icons 1.11.0
- **Backend**: FastAPI, Python
- **Database**: (To be configured)
- **Authentication**: Token-based with localStorage

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

3. Set up backend (optional - not yet fully implemented):
   ```bash
   cd backend
   # Configure database settings
   # Run migrations if applicable
   ```

## Usage

### Starting the Application
1. Open `frontend/pages/login.html` in a web browser
2. Log in with admin or student credentials
3. You'll be redirected to the appropriate dashboard based on your role

### Admin Workflow
- Log in as admin → Admin Dashboard → Manage students/courses/grades/etc.

### Student Workflow
- Log in as student → Student Dashboard → View courses, grades, attendance, assignments

## Color Scheme
- **Primary Gradient**: Purple (#667eea) to Blue (#764ba2)
- **Status Badges**: 
  - Green: Completed/Present
  - Yellow: Pending
  - Red: Failed/Absent
  - Blue: In Progress

## Current Status
- ✅ Frontend: Admin and Student dashboards with full UI
- ✅ Role-based routing and authentication
- ⏳ Backend: API endpoints (in development)
- ⏳ Database: Configuration (pending)

## Future Enhancements
- Backend API integration
- Database implementation
- Email notifications
- Advanced analytics and reporting
- File upload for documents

## License
MIT License
2. Use the navigation to access different features of the Student Management System.



## License
This project is licensed under the MIT License.