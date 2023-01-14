from src.domain.validators import UndoRedoValidator


class UndoRedoObject:
    def __init__(self, undo_function, redo_function):
        self.undo_function = undo_function
        self.redo_function = redo_function


class UndoRedoService:
    def __init__(self, student_repository, assignments_repository, grades_repository):
        self._student_repository = student_repository
        self._assignment_repository = assignments_repository
        self._grades_repository = grades_repository
        self._undo_redo_validator = UndoRedoValidator
        self._operations_stack = list()
        self._stack_pointer = 0

    def add_operation(self, operation):
        self._normalize_stack()
        self._operations_stack.append(operation)
        self._stack_pointer += 1

    def _normalize_stack(self):
        while len(self._operations_stack) != self._stack_pointer:
            self._operations_stack.pop()

    def undo(self):
        self._stack_pointer -= 1
        self._undo_redo_validator.validate_undo_bound(self._stack_pointer)
        self._operations_stack[self._stack_pointer].undo_function()

    def redo(self):
        self._undo_redo_validator.validate_redo_bound(self._stack_pointer, len(self._operations_stack))
        self._operations_stack[self._stack_pointer].redo_function()
        self._stack_pointer += 1

    def get_undo_redo_stack_operations(self):
        return list(self._operations_stack)
