class AnalyticsComponent:
    def __init__(self):
        print("Analytics component loaded")

analytics_component = AnalyticsComponent()

def render_enrollment_trends(data):
    """Render enrollment trends analytics"""
    if not data:
        return "<p>No enrollment data available</p>"
    
    return f"""
    <div class="analytics-card" style="background: white; padding: 20px; border-radius: 8px;">
        <h3>Enrollment Trends</h3>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <div>
                <p><strong>Total Courses:</strong> <span style="font-size: 24px; color: #667eea;">{data.get('total_courses', 0)}</span></p>
            </div>
            <div>
                <p><strong>Total Enrolled:</strong> <span style="font-size: 24px; color: #667eea;">{data.get('total_enrolled', 0)}</span></p>
            </div>
            <div>
                <p><strong>Average Enrollment:</strong> <span style="font-size: 24px; color: #667eea;">{data.get('average_enrollment', 0):.1f}</span></p>
            </div>
            <div>
                <p><strong>Courses at Capacity:</strong> <span style="font-size: 24px; color: #ff9800;">{data.get('courses_at_capacity', 0)}</span></p>
            </div>
        </div>
    </div>
    """

def render_attendance_patterns(data):
    """Render attendance patterns analytics"""
    if not data:
        return "<p>No attendance data available</p>"
    
    status_dist = data.get('status_distribution', {})
    present = status_dist.get('present', 0)
    absent = status_dist.get('absent', 0)
    late = status_dist.get('late', 0)
    excused = status_dist.get('excused', 0)
    
    return f"""
    <div class="analytics-card" style="background: white; padding: 20px; border-radius: 8px;">
        <h3>Attendance Patterns</h3>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <div>
                <p style="color: #388e3c;"><strong>Present:</strong> {present}</p>
                <p style="color: #d32f2f;"><strong>Absent:</strong> {absent}</p>
            </div>
            <div>
                <p style="color: #ff9800;"><strong>Late:</strong> {late}</p>
                <p style="color: #1976d2;"><strong>Excused:</strong> {excused}</p>
            </div>
        </div>
        <p style="margin-top: 15px;"><strong>Average Attendance:</strong> <span style="font-size: 24px; color: #667eea;">{data.get('average_attendance_percentage', 0):.1f}%</span></p>
    </div>
    """

def render_grade_distribution(data):
    """Render grade distribution analytics"""
    if not data:
        return "<p>No grade data available</p>"
    
    return f"""
    <div class="analytics-card" style="background: white; padding: 20px; border-radius: 8px;">
        <h3>Grade Distribution</h3>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <div>
                <p><strong>Total Grades:</strong> <span style="font-size: 24px; color: #667eea;">{data.get('total_grades', 0)}</span></p>
                <p><strong>Average Score:</strong> <span style="font-size: 24px; color: #667eea;">{data.get('average_score', 0):.2f}</span></p>
            </div>
            <div>
                <p><strong>Highest Score:</strong> <span style="font-size: 24px; color: #388e3c;">{data.get('highest_score', 0):.2f}</span></p>
                <p><strong>Lowest Score:</strong> <span style="font-size: 24px; color: #d32f2f;">{data.get('lowest_score', 0):.2f}</span></p>
            </div>
        </div>
        <p style="margin-top: 15px;"><strong>Median:</strong> {data.get('median_score', 0):.2f} | <strong>Std Deviation:</strong> {data.get('std_deviation', 0):.2f}</p>
    </div>
    """

def render_student_performance(data):
    """Render individual student performance analytics"""
    if not data:
        return "<p>No performance data available</p>"
    
    return f"""
    <div class="analytics-card" style="background: white; padding: 20px; border-radius: 8px;">
        <h3>Student Performance</h3>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <div>
                <p><strong>Student ID:</strong> {data.get('student_id', 'N/A')}</p>
                <p><strong>Courses Enrolled:</strong> <span style="font-size: 24px; color: #667eea;">{data.get('courses_enrolled', 0)}</span></p>
            </div>
            <div>
                <p><strong>Average Grade:</strong> <span style="font-size: 24px; color: #667eea;">{data.get('average_grade', 0):.2f}</span></p>
                <p><strong>Total Grades:</strong> <span style="font-size: 24px; color: #667eea;">{data.get('total_grades', 0)}</span></p>
            </div>
        </div>
        <p style="margin-top: 15px;"><strong>Average Attendance:</strong> {data.get('average_attendance', 0):.1f}% | <strong>Attendance Records:</strong> {data.get('attendance_records', 0)}</p>
    </div>
    """
