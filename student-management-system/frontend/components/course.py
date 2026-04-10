class CourseComponent:
    def __init__(self):
        print("Course component loaded")

course_component = CourseComponent()

def render_course_list(courses):
    """Render a table of courses"""
    if not courses:
        return "<p>No courses found</p>"
    
    rows = ""
    for course in courses:
        rows += f"""
        <tr>
            <td>{course.get('course_code', 'N/A')}</td>
            <td>{course.get('title', 'N/A')}</td>
            <td>{course.get('semester', 'N/A')}</td>
            <td>{course.get('year', 'N/A')}</td>
            <td>{course.get('credit_hours', 0)}</td>
            <td>{course.get('enrolled_count', 0)} / {course.get('max_seats', 0)}</td>
            <td>{course.get('status', 'N/A')}</td>
            <td>
                <button onclick="viewCourse('{course.get('id')}')">View</button>
                <button onclick="editCourse('{course.get('id')}')">Edit</button>
                <button onclick="deleteCourse('{course.get('id')}')">Delete</button>
            </td>
        </tr>
        """
    
    return f"""
    <table style="width: 100%; border-collapse: collapse;">
        <thead>
            <tr style="background: #f0f0f0;">
                <th style="padding: 10px; text-align: left;">Code</th>
                <th style="padding: 10px; text-align: left;">Title</th>
                <th style="padding: 10px; text-align: left;">Semester</th>
                <th style="padding: 10px; text-align: left;">Year</th>
                <th style="padding: 10px; text-align: left;">Credits</th>
                <th style="padding: 10px; text-align: left;">Enrollment</th>
                <th style="padding: 10px; text-align: left;">Status</th>
                <th style="padding: 10px; text-align: left;">Actions</th>
            </tr>
        </thead>
        <tbody>
            {rows}
        </tbody>
    </table>
    """

def render_course_detail(course):
    """Render detailed course information"""
    if not course:
        return "<p>Course not found</p>"
    
    schedule_days = ", ".join(course.get('schedule_days', []))
    
    return f"""
    <div class="course-detail" style="background: white; padding: 20px; border-radius: 8px;">
        <h2>{course.get('title', 'N/A')} ({course.get('course_code', 'N/A')})</h2>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <div>
                <p><strong>Description:</strong> {course.get('description', 'N/A')}</p>
                <p><strong>Credit Hours:</strong> {course.get('credit_hours', 0)}</p>
                <p><strong>Max Seats:</strong> {course.get('max_seats', 0)}</p>
                <p><strong>Enrolled Count:</strong> {course.get('enrolled_count', 0)}</p>
            </div>
            <div>
                <p><strong>Semester:</strong> {course.get('semester', 'N/A')}</p>
                <p><strong>Year:</strong> {course.get('year', 'N/A')}</p>
                <p><strong>Room Location:</strong> {course.get('room_location', 'N/A')}</p>
                <p><strong>Status:</strong> {course.get('status', 'N/A')}</p>
            </div>
        </div>
        <div style="margin-top: 20px;">
            <p><strong>Schedule:</strong></p>
            <p>Days: {schedule_days}</p>
            <p>Time: {course.get('start_time', 'N/A')} - {course.get('end_time', 'N/A')}</p>
        </div>
        <p style="color: #999; font-size: 12px;">Created: {course.get('created_at', 'N/A')} | Updated: {course.get('updated_at', 'N/A')}</p>
    </div>
    """
