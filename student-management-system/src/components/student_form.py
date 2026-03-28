class StudentForm:
    def __init__(self):
        self.student_data = {}

    def validate_input(self, name, student_id, courses, grades):
        if not name or not student_id:
            return False
        # Additional validation logic can be added here
        return True

    def submit_form(self, name, student_id, courses, grades):
        if self.validate_input(name, student_id, courses, grades):
            self.student_data = {
                'name': name,
                'student_id': student_id,
                'courses': courses,
                'grades': grades
            }
            self.update_student_profile()
            return True
        return False

    def update_student_profile(self):
        # Logic to update the student profile in the system
        pass

    def get_student_data(self):
        return self.student_data