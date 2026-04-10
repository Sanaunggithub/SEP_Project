class GradeComponent:
    def __init__(self):
        print("Grade component loaded")

grade_component = GradeComponent()

def render_grade_table(grades):
    """Render a table of grades"""
    if not grades:
        return "<p>No grades found</p>"
    
    rows = ""
    for grade in grades:
        rows += f"""
        <tr>
            <td>{grade.get('component_type', 'N/A')}</td>
            <td>{grade.get('score', 0)}</td>
            <td>{grade.get('max_score', 0)}</td>
            <td>{grade.get('weight', 0)}%</td>
            <td>{round((grade.get('score', 0) / grade.get('max_score', 1) * 100), 2)}%</td>
            <td>{grade.get('remarks', 'N/A')}</td>
            <td>
                <button onclick="editGrade('{grade.get('id')}')">Edit</button>
                <button onclick="deleteGrade('{grade.get('id')}')">Delete</button>
            </td>
        </tr>
        """
    
    return f"""
    <table style="width: 100%; border-collapse: collapse;">
        <thead>
            <tr style="background: #f0f0f0;">
                <th style="padding: 10px; text-align: left;">Component</th>
                <th style="padding: 10px; text-align: left;">Score</th>
                <th style="padding: 10px; text-align: left;">Max Score</th>
                <th style="padding: 10px; text-align: left;">Weight</th>
                <th style="padding: 10px; text-align: left;">Percentage</th>
                <th style="padding: 10px; text-align: left;">Remarks</th>
                <th style="padding: 10px; text-align: left;">Actions</th>
            </tr>
        </thead>
        <tbody>
            {rows}
        </tbody>
    </table>
    """

def render_gpa(gpa_data):
    """Render GPA information"""
    if not gpa_data:
        return "<p>GPA data not available</p>"
    
    gpa = gpa_data.get('gpa', 0)
    student_id = gpa_data.get('student_id', 'N/A')
    
    gpa_color = "#388e3c" if gpa >= 3.0 else "#ff9800" if gpa >= 2.0 else "#d32f2f"
    
    return f"""
    <div class="gpa-card" style="background: white; padding: 20px; border-radius: 8px; border-left: 5px solid {gpa_color};">
        <h3>Current GPA</h3>
        <div style="font-size: 48px; font-weight: bold; color: {gpa_color}; margin: 10px 0;">
            {gpa:.2f}
        </div>
        <p style="color: #666; margin: 0;">
            {'Excellent' if gpa >= 3.5 else 'Good' if gpa >= 3.0 else 'Satisfactory' if gpa >= 2.0 else 'Below Average'}
        </p>
        <p style="color: #999; font-size: 12px; margin-top: 10px;">Student ID: {student_id}</p>
    </div>
    """
