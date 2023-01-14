from src.domain.validators import AssignmentValidator
# from src.domain.assignment import Assignment
from src.utils_functions import Container


class AssignmentRepositoryException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)


class AssignmentRepository:
    def __init__(self):
        self.__assignments = Container(dict())
        self.__assignment_validator = AssignmentValidator

    def find_by_id(self, assignment_id):
        if assignment_id in self.__assignments:
            return self.__assignments[assignment_id]
        return None

    def save(self, assignment):
        if self.find_by_id(assignment.assignment_id) is not None:
            raise AssignmentRepositoryException(
                "There's already an assignment with id {0}".format(assignment.assignment_id))
        self.__assignment_validator.validate_description(assignment.description)
        self.__assignment_validator.validate_deadline(assignment.deadline)
        self.__assignments[assignment.assignment_id] = assignment

    def update(self, assignment_id, assignment):
        if self.find_by_id(assignment_id) is None:
            raise AssignmentRepositoryException(
                "There's no assignment with id {0}".format(assignment.assignment_id))
        self.__assignment_validator.validate_description(assignment.description)
        self.__assignment_validator.validate_deadline(assignment.deadline)
        self.__assignments[assignment.assignment_id] = assignment

    def delete_by_id(self, assignment_id):
        if self.find_by_id(assignment_id) is None:
            raise AssignmentRepositoryException(
                "There's no assignment with id {0}".format(assignment_id))
        del self.__assignments[assignment_id]

    def get_all(self):
        return list(self.__assignments.values())

# TESTS
# assignment_repository = AssignmentRepository()
#
#
# def run_assignment_repository_test():
#     save__id_not_exists__true()
#     save__id_not_exists__false()
#     save__valid_date_format__true()
#     save__valid_date_format__false()
#     save__description_is_string__true()
#     save__description_is_string__false()
#     update__id_exists__true()
#     update__id_exists__false()
#     delete__id_exists__true()
#     delete__id_exists__false()
#
#
# def save__id_not_exists__true():
#     new_assignment = Assignment(1, 'description', '2021-11-18')
#     try:
#         assignment_repository.save(new_assignment)
#         assert True
#     except AssignmentRepositoryException:
#         assert False
#
#
# def save__id_not_exists__false():
#     try:
#         new_assignment = Assignment(1, 'first', '2021-11-18')
#         assignment_repository.save(new_assignment)
#         new_assignment = Assignment(1, 'second', '2022-10-10')
#         assignment_repository.save(new_assignment)
#         assert False
#     except AssignmentRepositoryException:
#         assert True
#
#
# def save__valid_date_format__true():
#     try:
#         new_assignment = Assignment(2, 'description', '2022-03-20')
#         assignment_repository.save(new_assignment)
#         assert True
#     except Exception:
#         assert False
#
#
# def save__valid_date_format__false():
#     try:
#         new_assignment = Assignment(3, 'description', '2023/11/18')
#         assignment_repository.save(new_assignment)
#         assert False
#     except Exception:
#         assert True
#
#
# def save__description_is_string__true():
#     try:
#         new_assignment = Assignment(4, 'description', '2021-11-11')
#         assignment_repository.save(new_assignment)
#         assert True
#     except Exception:
#         assert False
#
#
# def save__description_is_string__false():
#     try:
#         new_assignment = Assignment(5, 23435, '2021-11-11')
#         assignment_repository.save(new_assignment)
#         assert False
#     except Exception:
#         assert True
#
#
# def update__id_exists__true():
#     try:
#         updated_assignment = Assignment(1, 'new description', '1999-10-10')
#         assignment_repository.update(1, updated_assignment)
#         assert True
#     except Exception:
#         assert False
#
#
# def update__id_exists__false():
#     try:
#         updated_assignment = Assignment(45, 'new description', '1999-10-10')
#         assignment_repository.update(45, updated_assignment)
#         assert False
#     except Exception:
#         assert True
#
#
# def delete__id_exists__true():
#     try:
#         assignment_id = 1
#         assignment_repository.delete_by_id(assignment_id)
#         assert True
#     except Exception:
#         assert False
#
#
# def delete__id_exists__false():
#     try:
#         assignment_id = 111
#         assignment_repository.delete_by_id(assignment_id)
#         assert False
#     except Exception:
#         assert True
#
#
# run_assignment_repository_test()
