class Assignment:
    def __init__(self, assignment_id, description, deadline):
        self.__assignment_id = assignment_id
        self.__description = description
        self.__deadline = deadline

    @property
    def assignment_id(self):
        return self.__assignment_id

    @assignment_id.setter
    def assignment_id(self, assignment_id_to_set):
        self.__assignment_id = assignment_id_to_set

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description_to_set):
        self.__description = description_to_set

    @property
    def deadline(self):
        return self.__deadline

    @deadline.setter
    def deadline(self, deadline_to_set):
        self.__deadline = deadline_to_set

    def __str__(self):
        return f"Assignment id: {self.__assignment_id}, " \
               f"Description: {self.__description}," \
               f" Deadline: {self.deadline}"
