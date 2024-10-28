import mongoengine
from mongoengine import *
from Student import Student
from Major import Major
from datetime import datetime


class StudentMajor(Document):
    student = ReferenceField(Student, required=True, reverse_delete_rule=mongoengine.DENY)
    major = ReferenceField(Major, required=True, reverse_delete_rule=mongoengine.DENY)
    da = DateTimeField(required=True)

    meta = {'collection': 'studentMajors',
            'indexes': [
                {'unique': True, 'fields': ['student', 'major'],
                 'name': 'studentMajors_pk_01'}]}

    def __init__(self, student: Student, major: Major, da: datetime, *args, **values):
        super().__init__(*args, **values)
        self.student = student
        self.major = major
        self.da = da

    def __str__(self):
        return f'Student: {self.student}\n{self.major}, \nDeclaration Date: {str(self.da)}'

    def get_major(self):
        return self.major

