from components.student_form import StudentForm
from components.student_list import StudentList
from components.student_details import StudentDetails
from components.navigation import Navigation
from services.student_service import StudentService
from services.data_manager import DataManager

class StudentManagementSystem:
    def __init__(self):
        self.student_service = StudentService()
        self.data_manager = DataManager()
        self.student_form = StudentForm(self.student_service)
        self.student_list = StudentList(self.student_service)
        self.student_details = StudentDetails(self.student_service)
        self.navigation = Navigation()

    def run(self):
        self.navigation.setup_navigation()
        self.student_list.render()
        self.student_form.render()

if __name__ == "__main__":
    app = StudentManagementSystem()
    app.run()