from src.domain.student import Student
from src.repository.base_repository.student_repository import StudentRepository


class StudentTextFileRepository(StudentRepository):
    def __init__(self, student_text_file):
        super().__init__()
        self._file_name = student_text_file
        self._load_file()

    def _load_file(self):
        file = open(self._file_name, "rt")  # rt -> read, text-mode
        for line in file.readlines():
            _id, name, group = line.split(maxsplit=2, sep=", ")
            self.save(Student(int(_id), str(name).rstrip(), int(group)))
        file.close()

    def _save_file(self):
        file = open(self._file_name, "wt")  # wt -> write, text-mode
        for student in super().get_all():
            file.writelines(f"{student.student_id}, {student.name}, {student.group}\n")
        file.close()

    def save(self, student):
        super(StudentTextFileRepository, self).save(student)
        self._save_file()

    def delete_by_id(self, student_id):
        super(StudentTextFileRepository, self).delete_by_id(student_id)
        self._save_file()

    def update(self, student_id, student):
        super(StudentTextFileRepository, self).update(student_id, student)
        self._save_file()

