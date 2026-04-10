class AssignmentComponent:
    def __init__(self):
        print("Assignment component loaded")

assignment_component = AssignmentComponent()

def render_assignment_list(assignments):
    """Render a table of assignments"""
    if not assignments:
        return "<p>No assignments found</p>"
    
    rows = ""
    for assignment in assignments:
        rows += f"""
        <tr>
            <td>{assignment.get('title', 'N/A')}</td>
            <td>{assignment.get('due_date', 'N/A')}</td>
            <td>{assignment.get('max_score', 0)}</td>
            <td>{'Yes' if assignment.get('allow_late_submission') else 'No'}</td>
            <td>{assignment.get('late_penalty_percent', 0)}%</td>
            <td>
                <button onclick="viewAssignment('{assignment.get('id')}')">View</button>
                <button onclick="editAssignment('{assignment.get('id')}')">Edit</button>
                <button onclick="deleteAssignment('{assignment.get('id')}')">Delete</button>
            </td>
        </tr>
        """
    
    return f"""
    <table style="width: 100%; border-collapse: collapse;">
        <thead>
            <tr style="background: #f0f0f0;">
                <th style="padding: 10px; text-align: left;">Title</th>
                <th style="padding: 10px; text-align: left;">Due Date</th>
                <th style="padding: 10px; text-align: left;">Max Score</th>
                <th style="padding: 10px; text-align: left;">Late Allowed</th>
                <th style="padding: 10px; text-align: left;">Late Penalty</th>
                <th style="padding: 10px; text-align: left;">Actions</th>
            </tr>
        </thead>
        <tbody>
            {rows}
        </tbody>
    </table>
    """

def render_submissions(submissions):
    """Render a table of assignment submissions"""
    if not submissions:
        return "<p>No submissions found</p>"
    
    rows = ""
    for submission in submissions:
        status_color = "#388e3c" if submission.get('status') == 'graded' else "#ff9800" if submission.get('status') == 'submitted' else "#d32f2f"
        rows += f"""
        <tr>
            <td>{submission.get('student_id', 'N/A')}</td>
            <td>{submission.get('submitted_at', 'N/A')}</td>
            <td>{'Late' if submission.get('is_late') else 'On Time'}</td>
            <td style="color: {status_color}; font-weight: bold;">{submission.get('status', 'N/A').upper()}</td>
            <td>{submission.get('score', 'N/A')}</td>
            <td>{submission.get('plagiarism_score', 'N/A')}</td>
            <td>
                <a href="{submission.get('file_url', '#')}" target="_blank">Download</a>
                <button onclick="gradeSubmission('{submission.get('id')}')">Grade</button>
                <button onclick="viewFeedback('{submission.get('id')}')">Feedback</button>
            </td>
        </tr>
        """
    
    return f"""
    <table style="width: 100%; border-collapse: collapse;">
        <thead>
            <tr style="background: #f0f0f0;">
                <th style="padding: 10px; text-align: left;">Student ID</th>
                <th style="padding: 10px; text-align: left;">Submitted At</th>
                <th style="padding: 10px; text-align: left;">Submission Type</th>
                <th style="padding: 10px; text-align: left;">Status</th>
                <th style="padding: 10px; text-align: left;">Score</th>
                <th style="padding: 10px; text-align: left;">Plagiarism</th>
                <th style="padding: 10px; text-align: left;">Actions</th>
            </tr>
        </thead>
        <tbody>
            {rows}
        </tbody>
    </table>
    """
