import pickle

from src.repository.base_repository.grade_repository import GradeRepository


class GradeBinaryFileRepository(GradeRepository):
    def __init__(self, student_repository, assignment_repository, grades_binary_file):
        super().__init__(student_repository, assignment_repository)
        self._file_name = grades_binary_file
        self._load_file()

    def _load_file(self):
        file = open(self._file_name, "rb")
        grades = pickle.load(file)
        for grade in grades:
            self.save(grade)
        file.close()

    def _save_file(self):
        file = open(self._file_name, "wb")
        pickle.dump(super().get_all(), file)
        file.close()

    def save(self, grade):
        super(GradeBinaryFileRepository, self).save(grade)
        self._save_file()

    def delete_grade(self, grade):
        super(GradeBinaryFileRepository, self).delete_grade(grade)
        self._save_file()

    def grade_assignment(self, grade):
        super(GradeBinaryFileRepository, self).grade_assignment(grade)
        self._save_file()