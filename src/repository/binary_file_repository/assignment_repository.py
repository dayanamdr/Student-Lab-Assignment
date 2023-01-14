import pickle

from src.repository.base_repository.assignment_repository import AssignmentRepository


class AssignmentBinaryFileRepository(AssignmentRepository):
    def __init__(self, assignments_binary_file):
        super().__init__()
        self._file_name = assignments_binary_file
        self._load_file()

    def _load_file(self):
        file = open(self._file_name, "rb")
        assignments = pickle.load(file)
        for assignment in assignments:
            self.save(assignment)
        file.close()

    def _save_file(self):
        file = open(self._file_name, "wb")
        pickle.dump(super().get_all(), file)
        file.close()

    def save(self, assignment):
        super(AssignmentBinaryFileRepository, self).save(assignment)
        self._save_file()

    def delete_by_id(self, assignment_id):
        super(AssignmentBinaryFileRepository, self).delete_by_id(assignment_id)
        self._save_file()

    def update(self, assignment_id, assignment):
        super(AssignmentBinaryFileRepository, self).update(assignment_id, assignment)
        self._save_file()