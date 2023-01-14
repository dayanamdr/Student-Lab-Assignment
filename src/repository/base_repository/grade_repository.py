from src.repository.base_repository.student_repository import StudentRepositoryException
from src.repository.base_repository.assignment_repository import AssignmentRepositoryException
from src.domain.validators import GradeValidator
from src.utils_functions import Container


class GradeRepositoryException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)


class GradeRepository:
    def __init__(self, student_repository, assignment_repository):
        self.__grades = Container(dict())
        self.__grade_validator = GradeValidator
        self.__student_repository = student_repository
        self.__assignment_repository = assignment_repository

    def find_by_student_and_assignment_ids(self, student_and_assignment_ids):
        if student_and_assignment_ids in self.__grades:
            return self.__grades[student_and_assignment_ids]
        return None

    def save(self, grade):
        if self.__student_repository.find_by_id(int(grade.student_id)) is None:
            raise StudentRepositoryException("There's no student with id {0}".format(grade.student_id))
        if self.__assignment_repository.find_by_id(int(grade.assignment_id)) is None:
            raise AssignmentRepositoryException("There's no assignment with id {0}".format(grade.assignment_id))
        student_and_assignment_ids = (int(grade.student_id), int(grade.assignment_id))
        if self.find_by_student_and_assignment_ids(student_and_assignment_ids) is not None:
            raise GradeRepositoryException(
                "There's already a grade with the student id {0} and assignment id {1}".format(
                    int(grade.student_id), int(grade.assignment_id)))
        self.__grades[student_and_assignment_ids] = grade

    def grade_assignment(self, grade):
        student_and_assignment_ids = (int(grade.student_id), int(grade.assignment_id))
        self.__grade_validator.validate_grade_value(grade.grade_value)
        self.__grades[student_and_assignment_ids] = grade

    def delete_grade(self, grade):
        student_and_assignment_ids = (int(grade.student_id), int(grade.assignment_id))
        if self.find_by_student_and_assignment_ids(student_and_assignment_ids) is None:
            raise GradeRepositoryException(
                "There's no student with id {0} and assignment with id {1}".format(
                    int(grade.student_id), int(grade.assignment_id)))
        del self.__grades[student_and_assignment_ids]

    def get_all(self):
        return list(self.__grades.values())
