from src.ui.ui import ConsoleCommand
from src.services.student_service import StudentService
from src.services.assignment_service import AssignmentService
from src.services.grade_service import GradeService
from src.services.undo_redo_service import UndoRedoService
from src.settings.settings import Settings

if __name__ == '__main__':
    student_repository, assignment_repository, grade_repository = Settings().set_repositories()

    undo_redo_service = UndoRedoService(student_repository, assignment_repository, grade_repository)
    grade_service = GradeService(grade_repository, student_repository, undo_redo_service)
    assignment_service = AssignmentService(assignment_repository, grade_repository, grade_service, undo_redo_service)
    student_service = StudentService(student_repository, grade_repository, grade_service, assignment_service,
                                     undo_redo_service)

    console = ConsoleCommand(student_service, assignment_service, grade_service, undo_redo_service)
    console.run_console()
