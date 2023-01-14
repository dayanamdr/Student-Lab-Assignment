from src.domain.assignment import Assignment
from src.domain.validators import AssignmentValidator
from src.services.undo_redo_service import UndoRedoObject
from datetime import *
from src.utils_functions import sort


class AssignmentService:
    def __init__(self, assignment_repository, grade_repository, grade_service, undo_redo_service):
        self.__assignment_repository = assignment_repository
        self.__grade_repository = grade_repository
        self.__assignment_validator = AssignmentValidator
        self.__grade_service = grade_service
        self.__undo_redo_service = undo_redo_service

    def add_assignment(self, assignment_id, assignment_description, assignment_deadline):
        new_assignment = Assignment(assignment_id, assignment_description, assignment_deadline)
        self.__assignment_repository.save(new_assignment)
        undo_redo_operation = UndoRedoObject(lambda: self.__assignment_repository.delete_by_id(assignment_id),
                                             lambda: self.__assignment_repository.save(new_assignment))
        self.__undo_redo_service.add_operation(undo_redo_operation)

    def update_assignment(self, assignment_id, assignment_description, assignment_deadline):
        current_assignment = self.__assignment_repository.find_by_id(assignment_id)
        update_assignment = Assignment(assignment_id, assignment_description, assignment_deadline)
        self.__assignment_repository.update(assignment_id, update_assignment)
        undo_redo_operation = UndoRedoObject(lambda: self.__assignment_repository.update(assignment_id, current_assignment),
                                             lambda: self.__assignment_repository.update(assignment_id, update_assignment))
        self.__undo_redo_service.add_operation(undo_redo_operation)

    def delete_assignment(self, assignment_id):
        # raises exception if there's not assignment with the given id
        self.__assignment_validator.validate_assignment_id_exists(assignment_id, self.get_all_assignments())
        assignment = self.__assignment_repository.find_by_id(assignment_id)
        assignment_grades = self.__grade_service.filter_grades_by_assignment_id(assignment_id)
        self.__assignment_repository.delete_by_id(assignment_id)
        self.__grade_service.delete_assignment_grades(assignment_id)


        def undo_function():
            self.__assignment_repository.save(assignment)
            for grade in assignment_grades:
                self.__grade_repository.save(grade)

        def redo_function():
            self.__assignment_repository.delete_by_id(assignment_id)
            for grade in assignment_grades:
                self.__grade_repository.delete_grade(grade)

        undo_redo_operation = UndoRedoObject(undo_function, redo_function)
        self.__undo_redo_service.add_operation(undo_redo_operation)

    def deadline_is_passed(self, assignment_id):
        # raises exception if there's not assignment with the given id
        self.__assignment_validator.validate_assignment_id_exists(assignment_id, self.get_all_assignments())
        for assignment in self.get_all_assignments():
            assignment_deadline = datetime.strptime(assignment.deadline, '%Y-%m-%d')
            if assignment_deadline < datetime.today() and assignment.assignment_id == assignment_id:
                return True
        return False

    def generate_assignments(self):
        for index in range(10):
            new_assignment = Assignment(index + 1, 'description', '2021-11-18')
            self.__assignment_repository.save(new_assignment)

    def get_all_assignments(self):
        return sort(self.__assignment_repository.get_all(), key=lambda assignment: assignment.assignment_id)
