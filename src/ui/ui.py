from src.settings.settings import Settings


class UserCommandException(Exception):
    def __init__(self, message):
        self.__message = message

    def __str__(self):
        return self.__message


class ConsoleCommand:
    def __init__(self, student_service, assignment_service, grade_service, undo_redo_service):
        self.__student_service = student_service
        self.__assignment_service = assignment_service
        self.__grade_service = grade_service
        self.__undo_redo_service = undo_redo_service
        self._repository_type = Settings().get_repository_type()

    def print_menu(self):
        menu_options = self.get_menu_options()
        print("Choose an option: ")
        for index in range(len(menu_options)):
            print(str(index + 1) + " - " + str(menu_options[index]))

    def print_students(self, students_list):
        self.print_list(students_list)

    def print_assignments(self, assignments_list):
        self.print_list(assignments_list)

    def print_grades(self, grades_list):
        self.print_list(grades_list)

    @staticmethod
    def print_students_top_by_average(students_list):
        for student in students_list:
            print(f"Student id: {student[0]}, Average: {student[1]}")

    # def print_student_ungraded_assignments(self, student_ungraded_assignments):
    #     self.print_list(student_ungraded_assignments)

    @staticmethod
    def get_menu_options():
        return ['add student', 'update student', 'delete student', 'list students', 'add assignment',
                'update assignment', 'delete assignment', 'list assignments', 'assign assignment to a student',
                'assign assignment to a group', 'list grades', 'grade student\'s assignment', 'delete student',
                'delete assignment', 'top students by grade for a given assignment', 'students with passed deadlines',
                'top students based on the average of grades', 'undo', 'redo', 'exit']

    def run_console(self):
        self.print_menu()
        if self._repository_type == "in-memory":
            self.__student_service.generate_students()
            self.__assignment_service.generate_assignments()
        while True:
            user_command = int(input("Enter an option: "))
            # if user_command == 20:
            #     break
            # self.execute_user_command(user_command)
            try:
                if user_command == 20:
                    break
                self.execute_user_command(user_command)
            except Exception as message:
                print(message)

    @staticmethod
    def get_student_input():
        student_id = int(input("Student id: "))
        student_name = input("Student name: ")
        student_group = int(input("Student group: "))
        return student_id, student_name, student_group

    @staticmethod
    def get_assignment_input():
        assignment_id = int(input("Assignment id: "))
        assignment_description = input("Assignment description: ")
        assignment_deadline = input("Assignment deadline with format YYYY-MM-DD: ")
        return assignment_id, assignment_description, assignment_deadline

    def execute_user_command(self, user_command):
        if user_command < 1 or user_command > len(self.get_menu_options()):
            raise UserCommandException("Enter a valid command!")
        if user_command == 1:
            student_id, student_name, student_group = self.get_student_input()
            self.__student_service.add_student(student_id, student_name, student_group)
        elif user_command == 2:
            student_id, student_name, student_group = self.get_student_input()
            self.__student_service.update_student(student_id, student_name, student_group)
        elif user_command == 3:
            student_id = int(input("Student id: "))
            self.__student_service.delete_student(student_id)
        elif user_command == 4:
            self.print_students(self.__student_service.get_all_students())
        elif user_command == 5:
            assignment_id, assignment_description, assignment_deadline = self.get_assignment_input()
            self.__assignment_service.add_assignment(assignment_id, assignment_description, assignment_deadline)
        elif user_command == 6:
            assignment_id, assignment_description, assignment_deadline = self.get_assignment_input()
            self.__assignment_service.update_assignment(assignment_id, assignment_description, assignment_deadline)
        elif user_command == 7:
            assignment_id = int(input("Assignment id: "))
            self.__assignment_service.delete_assignment(assignment_id)
        elif user_command == 8:
            self.print_assignments(self.__assignment_service.get_all_assignments())
        elif user_command == 9:
            student_id = int(input("Student id: "))
            assignment_id = int(input("Assignment id: "))
            self.__grade_service.assign_assignment_to_student(student_id, assignment_id)
        elif user_command == 10:
            group = int(input("Enter group: "))
            assignment_id = int(input("Assignment id: "))
            self.__grade_service.assign_assignment_to_group(group, assignment_id)
        elif user_command == 11:
            self.print_grades(self.__grade_service.get_all_grades())
        elif user_command == 12:
            student_id = int(input("Student id: "))
            student_ungraded_assignments = self.__grade_service.filter_student_ungraded_assignments(student_id)
            print("Ungraded assignments: ")
            self.print_grades(student_ungraded_assignments)
            assignment_id = int(input("Assignment id: "))
            grade_value = int(input("Grade value: "))
            self.__grade_service.grade_assignment(student_id, assignment_id, grade_value)
        elif user_command == 13:
            student_id = int(input("Student id: "))
            self.__student_service.delete_student(student_id)
        elif user_command == 14:
            assignment_id = int(input("Assignment id: "))
            self.__assignment_service.delete_assignment(assignment_id)
        elif user_command == 15:
            assignment_id = int(input("Assignment id: "))
            top_list = self.__student_service.top_students_by_assignment(assignment_id)
            self.print_grades(top_list)
        elif user_command == 16:
            students_list = self.__student_service.students_with_passed_deadlines()
            self.print_students(students_list)
        elif user_command == 17:
            students_list = self.__student_service.students_grades_average()
            self.print_students_top_by_average(students_list)
        elif user_command == 18:
            self.__undo_redo_service.undo()
        elif user_command == 19:
            self.__undo_redo_service.redo()

    @staticmethod
    def print_list(list_to_print):
        for item in list_to_print:
            print(item)
