class StudentDetails:
    def __init__(self, student):
        self.student = student

    def display_details(self):
        details = f"Name: {self.student.name}\n"
        details += f"ID: {self.student.id}\n"
        details += f"Courses: {', '.join(self.student.courses)}\n"
        details += f"Grades: {', '.join([f'{course}: {grade}' for course, grade in self.student.grades.items()])}\n"
        details += f"Attendance: {self.student.attendance}\n"
        return details

    def update_details(self, name=None, courses=None, grades=None, attendance=None):
        if name:
            self.student.name = name
        if courses:
            self.student.courses = courses
        if grades:
            self.student.grades.update(grades)
        if attendance is not None:
            self.student.attendance = attendance