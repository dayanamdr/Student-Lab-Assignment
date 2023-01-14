from src.domain.student import Student
from random import randint
from src.domain.validators import StudentValidator, AssignmentValidator
from src.services.undo_redo_service import UndoRedoObject
from src.utils_functions import sort


class StudentService:
    def __init__(self, student_repository, grade_repository, grade_service, assignment_service, undo_redo_service):
        self.__student_repository = student_repository
        self.__grade_repository = grade_repository
        self.__grade_service = grade_service
        self.__student_validator = StudentValidator
        self.__assignment_service = assignment_service
        self.__assignment_validator = AssignmentValidator
        self.__undo_redo_service = undo_redo_service

    def add_student(self, student_id, student_name, student_group):
        new_student = Student(student_id, student_name, student_group)
        self.__student_repository.save(new_student)
        undo_redo_operation = UndoRedoObject(lambda: self.__student_repository.delete_by_id(student_id),
                                             lambda: self.__student_repository.save(new_student))
        self.__undo_redo_service.add_operation(undo_redo_operation)

    def update_student(self, student_id, student_name, student_group):
        current_student = self.__student_repository.get_student_by_id(student_id)
        updated_student = Student(student_id, student_name, student_group)
        self.__student_repository.update(student_id, updated_student)
        undo_redo_operation = UndoRedoObject(lambda: self.__student_repository.update(student_id, current_student),
                                             lambda: self.__student_repository.update(student_id, updated_student))
        self.__undo_redo_service.add_operation(undo_redo_operation)

    def delete_student(self, student_id):
        # it raises exception if id doesn't exist
        self.__student_validator.validate_student_id_exists(student_id, self.get_all_students())
        student = self.__student_repository.find_by_id(student_id)
        student_grades = self.__grade_service.filter_grades_by_student_id(student_id)
        self.__student_repository.delete_by_id(student_id)
        self.__grade_service.delete_student_assignments(student_id)

        def undo_function():
            self.__student_repository.save(student)
            for grade in student_grades:
                self.__grade_repository.save(grade)

        def redo_function():
            self.__student_repository.delete_by_id(student_id)
            for grade in student_grades:
                self.__grade_repository.delete_grade(grade)

        undo_redo_operation = UndoRedoObject(undo_function, redo_function)
        self.__undo_redo_service.add_operation(undo_redo_operation)

    def top_students_by_assignment(self, assignment_id):
        self.__assignment_validator.validate_assignment_id_exists(assignment_id, self.__grade_repository.get_all())
        filtered_students_by_assignment = self.__grade_service.filter_grades_by_assignment_id(assignment_id)
        # filtered_students_by_assignment.sort(
        #     key=lambda grade: 0 if grade.grade_value is None else grade.grade_value, reverse=True)
        filtered_students_by_assignment = sort(filtered_students_by_assignment,
                                               key=lambda grade: 0 if grade.grade_value is None else grade.grade_value,
                                               reverse=True)
        return filtered_students_by_assignment

    def filter_students_by_passed_deadlines(self, grades_with_passed_deadlines):
        students_list = self.get_all_students()
        students_with_passed_deadlines = list()
        for student in students_list:
            if any(student.student_id == grade.student_id for grade in grades_with_passed_deadlines):
                students_with_passed_deadlines.append(student)
        return students_with_passed_deadlines

    def students_with_passed_deadlines(self):
        ungraded_assignments = self.__grade_service.filter_ungraded_assignments()
        assignments_with_passed_deadline = list()
        for grade in ungraded_assignments:
            if self.__assignment_service.deadline_is_passed(grade.assignment_id):
                assignments_with_passed_deadline.append(grade)
        students_list = self.filter_students_by_passed_deadlines(assignments_with_passed_deadline)
        return students_list

    def compute_students_average(self):
        students_list = self.get_all_students()
        students_grades_average = list()
        for student in students_list:
            student_grades = self.__grade_service.filter_grades_by_student_id(student.student_id)
            grades_sum = 0
            count_grades = 0
            for grade in student_grades:
                if grade.grade_value is not None:
                    grades_sum += grade.grade_value
                    count_grades += 1
            if count_grades != 0:
                student_average = grades_sum / count_grades
                students_grades_average.append((student.student_id, student_average))
        return students_grades_average

    def students_grades_average(self):
        students_average = self.compute_students_average()
        # students_average.sort(key=lambda element: element[1], reverse=True) -> previous method
        students_average = sort(students_average, key=lambda element: element[1], reverse=True)
        return students_average

    def generate_students(self):
        for index in range(10):
            new_student = Student(index + 1, 'Dayana', randint(1, 10))
            self.__student_repository.save(new_student)

    def get_all_students(self):
        return sort(self.__student_repository.get_all(), key=lambda student: student.student_id)
