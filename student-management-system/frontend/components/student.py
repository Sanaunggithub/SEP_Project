class StudentComponent:
    def __init__(self):
        print("Student component loaded")

student_component = StudentComponent()

def render_student_list(students):
    """Render a table of students"""
    if not students:
        return "<p>No students found</p>"
    
    rows = ""
    for student in students:
        rows += f"""
        <tr>
            <td>{student.get('full_name', 'N/A')}</td>
            <td>{student.get('student_id_number', 'N/A')}</td>
            <td>{student.get('program', 'N/A')}</td>
            <td>{student.get('department', 'N/A')}</td>
            <td>{student.get('year_level', 'N/A')}</td>
            <td>{student.get('scholarship_status', 'N/A')}</td>
            <td>{student.get('gpa', 0)}</td>
            <td>
                <button onclick="viewStudent('{student.get('id')}')">View</button>
                <button onclick="editStudent('{student.get('id')}')">Edit</button>
                <button onclick="deleteStudent('{student.get('id')}')">Delete</button>
            </td>
        </tr>
        """
    
    return f"""
    <table style="width: 100%; border-collapse: collapse;">
        <thead>
            <tr style="background: #f0f0f0;">
                <th style="padding: 10px; text-align: left;">Name</th>
                <th style="padding: 10px; text-align: left;">Student ID</th>
                <th style="padding: 10px; text-align: left;">Program</th>
                <th style="padding: 10px; text-align: left;">Department</th>
                <th style="padding: 10px; text-align: left;">Year Level</th>
                <th style="padding: 10px; text-align: left;">Scholarship</th>
                <th style="padding: 10px; text-align: left;">GPA</th>
                <th style="padding: 10px; text-align: left;">Actions</th>
            </tr>
        </thead>
        <tbody>
            {rows}
        </tbody>
    </table>
    """

def render_student_detail(student):
    """Render detailed student information"""
    if not student:
        return "<p>Student not found</p>"
    
    return f"""
    <div class="student-detail" style="background: white; padding: 20px; border-radius: 8px;">
        <h2>{student.get('full_name', 'N/A')}</h2>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <div>
                <p><strong>Student ID:</strong> {student.get('student_id_number', 'N/A')}</p>
                <p><strong>Program:</strong> {student.get('program', 'N/A')}</p>
                <p><strong>Department:</strong> {student.get('department', 'N/A')}</p>
                <p><strong>Year Level:</strong> {student.get('year_level', 'N/A')}</p>
            </div>
            <div>
                <p><strong>Scholarship Status:</strong> {student.get('scholarship_status', 'N/A')}</p>
                <p><strong>Academic Status:</strong> {student.get('academic_status', 'N/A')}</p>
                <p><strong>GPA:</strong> {student.get('gpa', 0)}</p>
                <p><strong>Active:</strong> {'Yes' if student.get('is_active') else 'No'}</p>
            </div>
        </div>
        <div style="margin-top: 20px;">
            <p><strong>Notes:</strong></p>
            <p>{student.get('notes', 'N/A')}</p>
        </div>
        <p style="color: #999; font-size: 12px;">Created: {student.get('created_at', 'N/A')} | Updated: {student.get('updated_at', 'N/A')}</p>
    </div>
    """
