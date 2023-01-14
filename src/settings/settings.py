from configparser import ConfigParser
from src.repository.base_repository.student_repository import StudentRepository
from src.repository.base_repository.assignment_repository import AssignmentRepository
from src.repository.base_repository.grade_repository import GradeRepository
from src.repository.binary_file_repository.assignment_repository import AssignmentBinaryFileRepository
from src.repository.binary_file_repository.grade_repository import GradeBinaryFileRepository
from src.repository.binary_file_repository.student_repository import StudentBinaryFileRepository
from src.repository.text_file_repository.assignment_repository import AssignmentTextFileRepository
from src.repository.text_file_repository.grade_repository import GradeTextFileRepository
from src.repository.text_file_repository.student_repository import StudentTextFileRepository


class Settings:
    def __init__(self):
        parser = ConfigParser()
        # use the path of your settings.properties file
        parser.read(r'C:\Users\dayana\Documents\Documents\uni2\an1\fp\a10-DayanaRalucaMardari\src\settings\settings.properties')
        self._repository_type = parser.get('options', 'repository')
        self._students_file = parser.get('options', 'students')
        self._assignments_file = parser.get('options', 'assignments')
        self._grades_file = parser.get('options', 'grades')

    def set_repositories(self):
        if self._repository_type == "in-memory":
            student_repository = StudentRepository()
            assignment_repository = AssignmentRepository()
            grade_repository = GradeRepository(student_repository, assignment_repository)
            return student_repository, assignment_repository, grade_repository
        elif self._repository_type == "text-files":
            student_repository = StudentTextFileRepository(self._students_file)
            assignment_repository = AssignmentTextFileRepository(self._assignments_file)
            grade_repository = GradeTextFileRepository(student_repository, assignment_repository, self._grades_file)
            return student_repository, assignment_repository, grade_repository
        elif self._repository_type == "binary-files":
            student_repository = StudentBinaryFileRepository(self._students_file)
            assignment_repository = AssignmentBinaryFileRepository(self._assignments_file)
            grade_repository = GradeBinaryFileRepository(student_repository, assignment_repository, self._grades_file)
            return student_repository, assignment_repository, grade_repository

    def get_repository_type(self):
        return self._repository_type
