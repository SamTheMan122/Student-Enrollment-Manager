from mongoengine import *
from Course import Course
from Student import Student

class Section(Document):
    """A catalog entry. Each course proposes to offer students who enroll in
    a section of the course an organized sequence of lessons and assignments
    aimed at teaching them specified skills."""
    department_abbreviation = StringField(required=True)
    course_number = IntField(required=True)
    course = ReferenceField(Course)
    enrollments = ListField(ReferenceField(Student))
    section_number = IntField(required=True)
    semester = StringField(required=True, choices=['Fall', 'Spring', 'Summer I', 'Summer II', 'Summer III', 'Winter'])
    section_year = IntField(required=True)
    building = StringField(required=True, choices=['NAC', 'CDC', 'DC', 'ECS', 'EN2', 'EN3', 'EN4', 'EN5', 'ET', 'HSCI', 'NUR', 'VEC'])
    room = IntField(required=True, min_value=1, max_value=999)
    schedule = StringField(choices=['MW', 'TuTh', 'MWF', 'F', 'S'])
    start_time = StringField(required=True)
    instructor = StringField(required=True)

    meta = {'collection': 'sections',
            'indexes': [
                {'unique': True, 'fields': ['course', 'section_number', 'semester', 'section_year'], 'name': 'sections_pk_01'},
                {'unique': True, 'fields': ['semester', 'section_year', 'building', 'room', 'schedule', 'start_time'], 'name': 'sections_pk_02'},
                {'unique': True, 'fields': ['semester', 'section_year', 'schedule', 'start_time'],
                 'name': 'sections_pk_03'}
            ]}

    def __init__(self, course: Course, section_number: int, semester: str, section_year: int, building: str, room: int, schedule: str, start_time: str, instructor: str, *args, **values):
        super().__init__(*args, **values)
        self.course = course
        self.department_abbreviation = course.department_abbreviation
        self.course_number = course.course_number
        self.section_number = section_number
        self.semester = semester
        self.section_year = section_year
        self.building = building
        self.room = room
        self.schedule = schedule
        self.start_time = start_time
        self.instructor = instructor
        self.enrollments = []

    def add_student(self, student):
        if student not in self.students:
            self.students.append(student)

    def remove_student(self, student):
        if student in self.students:
            self.students.remove(student)

    def __str__(self):
        return (f"{self.department_abbreviation} {self.course_number} section number: {self.section_number} "
                f"\nSemester: {self.semester} | Section Year: {self.section_year} | "
                f"Building: {self.building} Room: {self.room}"
                f"\nSchedule: {self.schedule} Start Time: {self.start_time}"
                f"\nInstructor: {self.instructor}")