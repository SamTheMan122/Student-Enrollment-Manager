from mongoengine import *

class Major(Document):
    """A distinct field of study. Each major has a degree program that a student
    can pursue towards a college diploma. Many universities offer specializations
    within a major to accommodate students who have a more focused set of
    objectives for their education. Several Departments have multiple majors.
    For instance, the CECS department has both a Computer Engineering as well as
    a Computer Science major."""
    # department = ReferenceField(Department, reverse_delete_rule=2)
    name = StringField(max_length=50, required=True)
    description = StringField(max_length=500, required=True)
    # students = ListField(ReferenceField('StudentMajor'))

    # def set_department(self, department: Department):
    #     self.department = department

    meta = {'collection': 'majors',
            'indexes': [
                {'unique': True, 'fields': ['name'],
                 'name': 'majors_pk_01'},
            ]}

    def __init__(self, name: str, description: str, *args, **values):
        super().__init__(*args, **values)
        # self.set_department(department)
        self.name = name
        self.description = description
        # self.students = []

    def add_student(self, student):
        if student not in self.students:
            self.students.append(student)

    def remove_student(self, student):
        if student in self.students:
            self.students.remove(student)

    def __str__(self):
        return f"Major Name: {self.name}\nMajor Description: {self.description}"