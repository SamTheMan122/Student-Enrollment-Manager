from mongoengine import *
import mongoengine

class Course(Document):
    """A catalog entry. Each course proposes to offer students who enroll in
    a section of the course an organized sequence of lessons and assignments
    aimed at teaching them specified skills."""
    course_number = IntField(required=True, min_value=100, max_value=699)
    sections = ListField(ReferenceField('Section'))
    name = StringField(required=True)
    description = StringField(required=True)
    units = IntField(required=True, min_value=1, max_value=4)
    department = ReferenceField('Department', required=True, reverse_delete_rule=mongoengine.DENY)
    department_abbreviation = StringField()

    meta = {'collection': 'courses',
            'indexes': [
                {'unique': True, 'fields': ['department_abbreviation', 'course_number'], 'name': 'courses_pk_01'},
                {'unique': True, 'fields': ['department_abbreviation', 'name'], 'name': 'courses_pk_02'}
            ]}

    def __init__(self, department, course_number: int, name: str, description: str, units: int, *args, **values):
        super().__init__(*args, **values)
        self.department = department
        self.department_abbreviation = self.department.abbreviation
        self.course_number = course_number
        self.name = name
        self.description = description
        self.units = units
        self.sections = []


    def add_section(self, section):
        if section not in self.sections:
            self.sections.append(section)

    def remove_section(self, section):
        if section in self.sections:
            self.sections.remove(section)

    def get_sections(self):
        return self.sections

    def __str__(self):
        return f"{self.name} \n{self.department_abbreviation} {self.course_number}  \nUnits: {self.units} \n{self.description}"