import datetime


class ValidatorException(Exception):
    def __init__(self, message):
        self.__message = message

    def __str__(self):
        return self.__message


class StudentValidator:
    @staticmethod
    def validate_name(name):
        if not str(name).isalpha():
            raise ValidatorException("Enter a valid name!")

    @staticmethod
    def validate_group(group):
        if not isinstance(group, int):
            raise ValidatorException("Enter a valid group name! Group needs to be an integer.")

    @staticmethod
    def validate_student_id_exists(student_id, students_list):
        if not any(student.student_id == student_id for student in students_list):
            raise ValidatorException("There's no student with id {0}".format(student_id))
        # if not any(student.student_id == student_id for student in students_list):
        #     raise ValidatorException("There's no student with id {0}".format(student_id))


class AssignmentValidator:
    @staticmethod
    def validate_description(description):
        if not isinstance(description, str):
            raise ValidatorException("Enter a valid description! Description needs to be a string.")

    @staticmethod
    def validate_deadline(deadline):
        try:
            datetime.datetime.strptime(deadline, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Incorrect data format, it should be YYYY-MM-DD")

    @staticmethod
    def validate_assignment_id_exists(assignment_id, assignments_list):
        if not any(assignment.assignment_id == assignment_id for assignment in assignments_list):
            raise ValidatorException("There's no assignment with id {0}".format(assignment_id))


class GradeValidator:
    @staticmethod
    def validate_grade_value(grade_value):
        if grade_value is not None and (grade_value < 0 or grade_value > 10):
            raise ValidatorException("Enter a valid grade with value between 1 and 10.")

    @staticmethod
    def validate_grade(grade):
        if not isinstance(grade, int):
            raise ValidatorException("Enter a valid grade! Grade needs to be an integer.")

    @staticmethod
    def validate_grade_exists(student_id, assignment_id, grades_list):
        if not any(grade.student_id == student_id and grade.assignment_id == assignment_id for grade in grades_list):
            raise ValidatorException(
                "There's no assignment with student id {0} and assignment id {1}".format(student_id, assignment_id))

    @staticmethod
    def validate_assignment_is_ungraded(student_id, assignment_id, grades_list):
        if any(grade.student_id == student_id and grade.assignment_id == assignment_id
               and grade.grade_value is not None for grade in grades_list):
            raise ValidatorException("The assignment {0} for student with id {1} "
                                     "has already been graded".format(assignment_id, student_id))

    @staticmethod
    def validate_grade_with_assignment_id_exists(assignment_id, grades_list):
        if not any(grade.assignment_id == assignment_id for grade in grades_list):
            raise ValidatorException("There's no assignment in grades list with id {0}".format(assignment_id))

    @staticmethod
    def validate_grade_with_student_id_exists(student_id, grades_list):
        if not any(grade.student_id == student_id for grade in grades_list):
            raise ValidatorException("There's no student in grades list with id {0}".format(student_id))


class UndoRedoValidator:
    @staticmethod
    def validate_undo_bound(stack_pointer):
        if stack_pointer < 0:
            raise ValidatorException("There's no operation to undo")

    @staticmethod
    def validate_redo_bound(stack_pointer, stack_length):
        if stack_pointer == stack_length:
            raise ValidatorException("There's no operation to redo")
