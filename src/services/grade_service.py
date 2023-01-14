from src.domain.grade import Grade
from src.domain.validators import GradeValidator, AssignmentValidator
from src.services.undo_redo_service import UndoRedoObject
from src.utils_functions import sort, filter_list

class GradeService:
    def __init__(self, grade_repository, student_repository, undo_redo_service):
        self.__grade_repository = grade_repository
        self.__student_repository = student_repository
        self.__grade_validator = GradeValidator
        self.__assignment_validator = AssignmentValidator
        self.__undo_redo_service = undo_redo_service

    def assign_assignment_to_student(self, student_id, assignment_id):
        new_assignment_to_student = Grade(assignment_id, student_id)
        self.__grade_repository.save(new_assignment_to_student)
        undo_redo_operation = UndoRedoObject(lambda: self.__grade_repository.delete_grade(new_assignment_to_student),
                                             lambda: self.__grade_repository.save(new_assignment_to_student))
        self.__undo_redo_service.add_operation(undo_redo_operation)

    def assign_assignment_to_group(self, group, assignment_id):
        group_students = self.__student_repository.filter_students_by_group(group)
        new_assignments = list()
        for student in group_students:
            to_search_for = (group_students[student].student_id, assignment_id)
            if self.__grade_repository.find_by_student_and_assignment_ids(to_search_for) is None:
                new_assignment_to_student = Grade(assignment_id, group_students[student].student_id)
                self.__grade_repository.save(new_assignment_to_student)
                new_assignments.append(new_assignment_to_student)

        def undo_function():
            for grade in new_assignments:
                self.__grade_repository.delete_grade(grade)

        def redo_function():
            for grade in new_assignments:
                self.__grade_repository.save(grade)

        undo_redo_operation = UndoRedoObject(undo_function, redo_function)
        self.__undo_redo_service.add_operation(undo_redo_operation)

    def filter_grades_by_student_id(self, student_id):
        # return list(filter(lambda grade: grade.student_id == student_id, self.get_all_grades()))
        return list(filter_list(self.get_all_grades(), lambda grade: grade.student_id == student_id))

    def filter_grades_by_assignment_id(self, assignment_id):
        # return list(filter(lambda grade: grade.assignment_id == assignment_id, self.get_all_grades()))
        return list(filter_list(self.get_all_grades(), lambda grade: grade.assignment_id == assignment_id))

    def filter_ungraded_assignments(self):
        # return list(filter(lambda grade: grade.grade_value is None, self.get_all_grades()))
        return list(filter_list(self.get_all_grades(), lambda grade: grade.grade_value is None))

    def filter_student_ungraded_assignments(self, student_id):
        # check if there exists any grade with this id
        self.__grade_validator.validate_grade_with_student_id_exists(student_id, self.get_all_grades())
        student_assignments = self.filter_grades_by_student_id(student_id)
        # return list(filter(lambda grade: grade.grade_value is None, student_assignments))
        return list(filter_list(student_assignments, lambda grade: grade.grade_value is None))

    def grade_assignment(self, student_id, assignment_id, grade_value):
        self.__grade_validator.validate_grade_exists(student_id, assignment_id, self.get_all_grades())
        self.__grade_validator.validate_assignment_is_ungraded(student_id, assignment_id, self.get_all_grades())
        old_grade = self.__grade_repository.find_by_student_and_assignment_ids((student_id, assignment_id))
        grade = Grade(assignment_id, student_id, grade_value)
        self.__grade_repository.grade_assignment(grade)

        undo_redo_operation = UndoRedoObject(lambda: self.__grade_repository.grade_assignment(old_grade),
                                             lambda: self.__grade_repository.grade_assignment(grade))
        self.__undo_redo_service.add_operation(undo_redo_operation)

    def delete_student_assignments(self, student_id):
        # student id is already validated in StudentService
        student_assignments = self.filter_grades_by_student_id(student_id)
        for grade in student_assignments:
            self.__grade_repository.delete_grade(grade)

    def delete_assignment_grades(self, assignment_id):
        # assignment id is already validated in AssignmentService
        assignment_grades = self.filter_grades_by_assignment_id(assignment_id)
        for grade in assignment_grades:
            self.__grade_repository.delete_grade(grade)

    def get_all_grades(self):
        def sort_function(grade1, grade2):
            if grade1.student_id < grade2.student_id:
                return True
            if grade1.student_id == grade2.student_id and grade1.assignment_id < grade2.assignment_id:
                return True
            return False
        return sort(self.__grade_repository.get_all(), function=sort_function)
