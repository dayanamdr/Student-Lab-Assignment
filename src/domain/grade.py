class Grade:
    def __init__(self, assignment_id, student_id, grade_value=None):
        self.__assignment_id = assignment_id
        self.__student_id = student_id
        self.__grade_value = grade_value

    @property
    def assignment_id(self):
        return self.__assignment_id

    @assignment_id.setter
    def assignment_id(self, assignment_id_to_set):
        self.__assignment_id = assignment_id_to_set

    @property
    def student_id(self):
        return self.__student_id

    @student_id.setter
    def student_id(self, student_id_to_set):
        self.__student_id = student_id_to_set

    @property
    def grade_value(self):
        return self.__grade_value

    @grade_value.setter
    def grade_value(self, grade_value_to_set):
        self.__grade_value = grade_value_to_set

    def __str__(self):
        return f"Student id: {self.__student_id}," \
               f" Assignment id: {self.__assignment_id}, " \
               f"Grade value: {self.__grade_value}"
