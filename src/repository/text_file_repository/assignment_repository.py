from src.domain.assignment import Assignment
from src.repository.base_repository.assignment_repository import AssignmentRepository


class AssignmentTextFileRepository(AssignmentRepository):
    def __init__(self, students_text_file):
        super().__init__()
        self._file_name = students_text_file
        self._load_file()

    def _load_file(self):
        file = open(self._file_name, "rt")
        for line in file.readlines():
            _id, description, str_deadline = line.split(maxsplit=2, sep=", ")
            self.save(Assignment(int(_id), str(description).rstrip(), str(str_deadline).rstrip()))
        file.close()

    def _save_file(self):
        file = open(self._file_name, "wt")
        for assignment in super().get_all():
            file.writelines(f"{assignment.assignment_id}, {assignment.description}, {assignment.deadline}\n")
        file.close()

    def save(self, assignment):
        super(AssignmentTextFileRepository, self).save(assignment)
        self._save_file()

    def delete_by_id(self, assignment_id):
        super(AssignmentTextFileRepository, self).delete_by_id(assignment_id)
        self._save_file()

    def update(self, assignment_id, assignment):
        super(AssignmentTextFileRepository, self).update(assignment_id, assignment)
        self._save_file()
