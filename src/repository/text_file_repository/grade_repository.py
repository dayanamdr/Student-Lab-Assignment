from src.domain.grade import Grade
from src.repository.base_repository.grade_repository import GradeRepository


class GradeTextFileRepository(GradeRepository):
    def __init__(self, student_repository, assignment_repository, grades_text_file):
        super().__init__(student_repository, assignment_repository)
        self._file_name = grades_text_file
        self._load_file()

    def _load_file(self):
        file = open(self._file_name, "rt")
        for line in file.readlines():
            _student_id, _assignment_id, grade_value = line.split(maxsplit=2, sep=", ")
            if grade_value == "None\n":
                grade_value = None
            else:
                grade_value = int(grade_value)
            self.save(Grade(int(_assignment_id), int(_student_id), grade_value))
        file.close()

    def _save_file(self):
        file = open(self._file_name, "wt")
        for grade in super().get_all():
            file.writelines(f"{grade.student_id}, {grade.assignment_id}, {grade.grade_value}\n")
        file.close()

    def save(self, grade):
        super(GradeTextFileRepository, self).save(grade)
        self._save_file()

    def delete_grade(self, grade):
        super(GradeTextFileRepository, self).delete_grade(grade)
        self._save_file()

    def grade_assignment(self, grade):
        super(GradeTextFileRepository, self).grade_assignment(grade)
        self._save_file()

