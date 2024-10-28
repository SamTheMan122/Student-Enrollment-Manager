from mongoengine import *


class Department(Document):
    abbreviation = StringField(required=True, max_length=6)
    name = StringField(required=True, max_length=50)
    chair_name = StringField(required=True, max_length=80)
    building = StringField(required=True, choices=['NAC', 'CDC', 'DC', 'ECS', 'EN2', 'EN3', 'EN4', 'EN5', 'ET', 'HSCI', 'NUR', 'VEC', 'COB', 'AS', 'EED', 'ET', 'HSCI', 'FND'])
    office = IntField(required=True)
    description = StringField(required=True, max_length=500)

    majors = ListField(ReferenceField('Major'))
    courses = ListField(ReferenceField('Course'))

    meta = {'collection': 'departments',
            'indexes': [
                {'unique': True, 'fields': ['chair_name'], 'name': 'departments_pk_01'},
                {'unique': True, 'fields': ['building', 'office'], 'name': 'departments_pk_02'},
                {'unique': True, 'fields': ['name'], 'name': 'departments_pk_03'},
                {'unique': True, 'fields': ['abbreviation'], 'name': 'departments_pk_04'}
            ]}

    def __init__(self, abbreviation: str, name: str, chair_name: str, building: str, office: int, description: str, *args, **values):
        super().__init__(*args, **values)
        self.abbreviation = abbreviation
        self.name = name
        self.chair_name = chair_name
        self.building = building
        self.office = office
        self.description = description
        self.majors = []
        self.courses = []

    def add_course(self, course):
        self.courses.append(course)
        self.save()

    def remove_course(self, course):
        if course in self.courses:
            self.courses.remove(course)

    def get_courses(self):
        return self.courses

    def __str__(self):
        return (f"Name: {self.name} \n"
                f"Abbreviation: {self.abbreviation} \n"
                f"Chair Name: {self.chair_name}\n"
                f"Building/Office: {self.building} {self.office}\n"
                f"Description: {self.description}")