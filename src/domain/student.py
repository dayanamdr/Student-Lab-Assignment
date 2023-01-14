class Student:
    def __init__(self, student_id, name, group):
        self.__student_id = student_id
        self.__name = name
        self.__group = group

    @property
    def student_id(self):
        return self.__student_id

    @student_id.setter
    def student_id(self, id_to_set):
        self.__student_id = id_to_set

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name_to_set):
        self.__name = name_to_set

    @property
    def group(self):
        return self.__group

    @group.setter
    def group(self, group_to_set):
        self.__group = group_to_set

    def __str__(self):
        return f"Student id: {self.__student_id}, " \
               f"Name: {self.__name}, " \
               f"Group: {self.__group}"