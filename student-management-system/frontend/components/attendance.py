class AttendanceComponent:
    def __init__(self):
        print("Attendance component loaded")

attendance_component = AttendanceComponent()

def render_attendance_table(records):
    """Render a table of attendance records"""
    if not records:
        return "<p>No attendance records found</p>"
    
    rows = ""
    for record in records:
        status_color = "#388e3c" if record.get('status') == 'present' else "#d32f2f" if record.get('status') == 'absent' else "#ff9800"
        rows += f"""
        <tr>
            <td>{record.get('student_id', 'N/A')}</td>
            <td>{record.get('date', 'N/A')}</td>
            <td style="color: {status_color}; font-weight: bold;">{record.get('status', 'N/A').upper()}</td>
            <td>{record.get('check_in_time', 'N/A')}</td>
            <td>{record.get('marked_by', 'N/A')}</td>
            <td>
                <button onclick="updateAttendance('{record.get('id')}', 'present')">Present</button>
                <button onclick="updateAttendance('{record.get('id')}', 'absent')">Absent</button>
                <button onclick="updateAttendance('{record.get('id')}', 'late')">Late</button>
            </td>
        </tr>
        """
    
    return f"""
    <table style="width: 100%; border-collapse: collapse;">
        <thead>
            <tr style="background: #f0f0f0;">
                <th style="padding: 10px; text-align: left;">Student ID</th>
                <th style="padding: 10px; text-align: left;">Date</th>
                <th style="padding: 10px; text-align: left;">Status</th>
                <th style="padding: 10px; text-align: left;">Check-in Time</th>
                <th style="padding: 10px; text-align: left;">Marked By</th>
                <th style="padding: 10px; text-align: left;">Actions</th>
            </tr>
        </thead>
        <tbody>
            {rows}
        </tbody>
    </table>
    """

def render_at_risk(students):
    """Render a list of at-risk students with low attendance"""
    if not students:
        return "<p>No at-risk students</p>"
    
    cards = ""
    for student in students:
        attendance_rate = student.get('attendance_rate', 0)
        cards += f"""
        <div style="background: #ffebee; padding: 15px; border-radius: 8px; margin-bottom: 10px; border-left: 5px solid #d32f2f;">
            <h4 style="margin: 0 0 5px 0; color: #d32f2f;">{student.get('full_name', 'N/A')}</h4>
            <p style="margin: 5px 0; color: #666;"><strong>Student ID:</strong> {student.get('student_id_number', 'N/A')}</p>
            <p style="margin: 5px 0; color: #d32f2f;"><strong>Attendance Rate:</strong> {attendance_rate:.1f}%</p>
            <button onclick="contactStudent('{student.get('id')}')">Contact Student</button>
        </div>
        """
    
    return f"""
    <div class="at-risk-list">
        <h3>At-Risk Students (Below 75% Attendance)</h3>
        {cards}
    </div>
    """
