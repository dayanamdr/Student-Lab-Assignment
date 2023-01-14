from src.domain.validators import StudentValidator
# from src.domain.student import Student
from src.utils_functions import Container


class StudentRepositoryException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)


class StudentRepository:
    def __init__(self):
        self.__students = Container(dict())
        self.__student_validator = StudentValidator

    def get_student_by_id(self, student_id):
        return self.__students[student_id]

    def find_by_id(self, student_id):
        if student_id in self.__students:
            return self.__students[student_id]
        return None

    def check_group_existence(self, group_to_search):
        for student in self.__students:
            if group_to_search == self.__students[student].group:
                return True
        return False

    def save(self, student):
        if self.find_by_id(student.student_id) is not None:
            raise StudentRepositoryException(
                "There's already a student with id {0}".format(student.student_id))
        self.__student_validator.validate_name(student.name)
        self.__student_validator.validate_group(student.group)
        self.__students[student.student_id] = student

    def update(self, student_id, student):
        print(self.get_all())
        if self.find_by_id(student_id) is None:
            raise StudentRepositoryException("There's no student with id {0}".format(student_id))
        self.__student_validator.validate_name(student.name)
        self.__student_validator.validate_group(student.group)
        self.__students[student.student_id] = student

    def delete_by_id(self, student_id):
        del self.__students[student_id]

    def filter_students_by_group(self, student_group):
        if self.check_group_existence(student_group) is False:
            raise StudentRepositoryException("There's no student with group {0}".format(student_group))
        filtered_students_by_group = {}
        for (student, data) in self.__students.items():
            if student_group == data.group:
                student_id = data.student_id
                filtered_students_by_group[student_id] = data
        return filtered_students_by_group

    def get_all(self):
        return list(self.__students.values())

#TESTS
# student_repository = StudentRepository()
#
#
# def run_student_repository_tests():
#     save__new_student__true()
#     save__new_student__false()
#     save__name_is_valid__true()
#     save__name_is_valid__false()
#     save__group_is_int__true()
#     save__group_is_int__false()
#     update__student_data__true()
#     update__student_date__false()
#     filter_students_by_group__valid_group__true()
#     filter_students_by_group__valid_group__false()
#     delete__valid_id__true()
#     delete__valid_id__false()
#
#
# def save__new_student__true():
#     try:
#         new_student = Student(1, 'Dayana', 123)
#         student_repository.save(new_student)
#         assert True
#     except StudentRepositoryException:
#         assert False
#
#
# def save__new_student__false():
#     try:
#         new_student = Student(2, 'Dayana', 12)
#         student_repository.save(new_student)
#         new_student = Student(2, 'Ioana', 34)
#         student_repository.save(new_student)
#         assert False
#     except StudentRepositoryException:
#         assert True
#
#
# def save__name_is_valid__true():
#     try:
#         new_student = Student(3, 'Dayana', 464)
#         student_repository.save(new_student)
#         assert True
#     except Exception:
#         assert False
#
#
# def save__name_is_valid__false():
#     try:
#         new_student = Student(4, 'Da4yana', 464)
#         student_repository.save(new_student)
#         assert False
#     except Exception:
#         assert True
#
#
# def save__group_is_int__true():
#     try:
#         new_student = Student(5, 'Dayana', 333)
#         student_repository.save(new_student)
#         assert True
#     except Exception:
#         assert False
#
#
# def save__group_is_int__false():
#     try:
#         new_student = Student(6, 'Dayana', '345')
#         student_repository.save(new_student)
#         assert False
#     except Exception:
#         assert True
#
#
# def update__student_data__true():
#     try:
#         new_student = Student(7, 'Dayana', 123)
#         student_repository.save(new_student)
#         updated_student = Student(7, 'Ioana', 345)
#         student_repository.update(7, updated_student)
#         assert True
#     except Exception:
#         assert False
#
#
# def update__student_date__false():
#     new_student = Student(8, 'Dayana', 123)
#     student_repository.save(new_student)
#     # non-existing id
#     try:
#         updated_student = Student(1234, 'Ioana', 345)
#         student_repository.update(1234, updated_student)
#         assert False
#     except Exception:
#         assert True
#
#     # invalid name
#     try:
#         updated_student = Student(8, 'Ioa345na', 345)
#         student_repository.update(8, updated_student)
#         assert False
#     except Exception:
#         assert True
#
#     # invalid group
#     try:
#         updated_student = Student(8, 'Ioana', '34567')
#         student_repository.update(8, updated_student)
#         assert False
#     except Exception:
#         assert True
#
#
# def filter_students_by_group__valid_group__true():
#     group = 345
#     try:
#         filtered_students = student_repository.filter_students_by_group(group)
#         assert 7 in filtered_students  # student with id 7 is in group 345
#         assert True
#     except Exception:
#         assert False
#
#
# def filter_students_by_group__valid_group__false():
#     group = 3366
#     try:
#         filtered_students = student_repository.filter_students_by_group(group)
#         assert False
#     except Exception:
#         assert True
#
#
# def delete__valid_id__true():
#     student_id = 1
#     try:
#         student_repository.delete_by_id(student_id)
#         assert 1 not in student_repository.get_all()
#         assert True
#     except Exception:
#         assert False
#
#
# def delete__valid_id__false():
#     student_id = 1212
#     try:
#         student_repository.delete_by_id(student_id)
#         assert False
#     except Exception:
#         assert True
#
#
# run_student_repository_tests()
