class StudentList:
    def __init__(self, student_service):
        self.student_service = student_service
        self.students = []

    def fetch_students(self):
        self.students = self.student_service.get_all_students()

    def render(self):
        student_list_html = "<ul>"
        for student in self.students:
            student_list_html += f"<li>{student.name} (ID: {student.id})</li>"
        student_list_html += "</ul>"
        return student_list_html

    def update_student_list(self):
        self.fetch_students()
        return self.render()