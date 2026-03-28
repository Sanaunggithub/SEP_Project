class Student:
    def __init__(self, name, student_id, courses=None, grades=None, attendance=None):
        self.name = name
        self.student_id = student_id
        self.courses = courses if courses is not None else []
        self.grades = grades if grades is not None else {}
        self.attendance = attendance if attendance is not None else {}

    def add_course(self, course):
        if course not in self.courses:
            self.courses.append(course)

    def update_grade(self, course, grade):
        self.grades[course] = grade

    def update_attendance(self, date, status):
        self.attendance[date] = status

    def get_average_grade(self):
        if not self.grades:
            return 0
        return sum(self.grades.values()) / len(self.grades)

    def __str__(self):
        return f"Student(Name: {self.name}, ID: {self.student_id}, Courses: {self.courses})"