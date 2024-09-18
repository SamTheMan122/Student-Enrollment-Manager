from mongoengine import *
from Major import Major

class Student(Document):
    """An individual who may or may not be enrolled at the university, who
    enrolls in courses toward some educational objective. That objective
    could be a formal degree program, or it could be a specialized certificate."""
    lastName = StringField(required=True)
    firstName = StringField(required=True)
    email = StringField(required=True)
    studentMajors = ListField(ReferenceField(Major))
    meta = {'collection': 'students',
            'indexes': [
                {'unique': True, 'fields': ['lastName', 'firstName'],
                 'name': 'students_pk_01'},
                {'unique': True, 'fields': ['email'],
                 'name': 'students_pk_02'}
            ]}

    def __init__(self, lastName: str, firstName: str, email: str, *args, **values):
        super().__init__(*args, **values)
        self.lastName = lastName
        self.firstName = firstName
        self.email = email
        self.studentMajors = []
        # self.sections = []

    def add_major(self, major):
        if major not in self.majors:
            self.majors.append(major)

    def remove_major(self, major):
        if major in self.majors:
            self.majors.remove(major)

    # def add_section(self, section):
    #     if section not in self.sections:
    #         self.sections.append(section)
    #
    # def remove_section(self, section):
    #     if section in self.sections:
    #         self.sections.remove(section)

    def __str__(self):
        return f"Student ID: {self.id} name: {self.lastName}, {self.firstName} e-mail: {self.email}"