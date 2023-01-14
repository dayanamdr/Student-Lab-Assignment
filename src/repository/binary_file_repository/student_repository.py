from src.repository.base_repository.student_repository import StudentRepository
import pickle


class StudentBinaryFileRepository(StudentRepository):
    def __init__(self, students_binary_file):
        super().__init__()
        self._file_name = students_binary_file
        self._load_file()

    def _load_file(self):
        file = open(self._file_name, "rb")  # rb -> read, binary
        students = pickle.load(file)
        for student in students:
            self.save(student)
        file.close()

    def _save_file(self):
        file = open(self._file_name, "wb")
        pickle.dump(super().get_all(), file)
        file.close()

    def save(self, student):
        super(StudentBinaryFileRepository, self).save(student)
        self._save_file()

    def delete_by_id(self, student_id):
        super(StudentBinaryFileRepository, self).delete_by_id(student_id)
        self._save_file()

    def update(self, student_id, student):
        super(StudentBinaryFileRepository, self).update(student_id, student)
        self._save_file()

