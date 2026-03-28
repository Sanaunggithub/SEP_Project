from models.student import Student

class StudentService:
    def __init__(self):
        self.students = []

    def add_student(self, student: Student):
        self.students.append(student)

    def update_student(self, student_id: int, updated_student: Student):
        for index, student in enumerate(self.students):
            if student.id == student_id:
                self.students[index] = updated_student
                return True
        return False

    def get_student(self, student_id: int) -> Student:
        for student in self.students:
            if student.id == student_id:
                return student
        return None

    def get_all_students(self) -> list:
        return self.students.copy()