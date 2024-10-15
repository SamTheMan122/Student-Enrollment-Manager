from ConstraintUtilities import select_general, unique_general, prompt_for_date
from Utilities import Utilities
from Department import Department
from Course import Course
from Section import Section
from Major import Major
from Student import Student
from StudentMajor import StudentMajor
from datetime import time
from CommandLogger import CommandLogger, log
from pymongo import monitoring
from Menu import Menu
from Option import Option
from menu_definitions import menu_main, add_select, list_select, delete_select
from datetime import date
# OrderItem.register_delete_rule(Order, 'orderItems', mongoengine.DENY)

def menu_loop(menu: Menu):
    """Little helper routine to just keep cycling in a menu until the user signals that they
    want to exit.
    :param  menu:   The menu that the user will see."""
    action: str = ''
    while action != menu.last_action():
        action = menu.menu_prompt()
        print('next action: ', action)
        exec(action)

def add():
    menu_loop(add_select)

def list_members():
    menu_loop(list_select)

def delete():
    menu_loop(delete_select)

def select_department() -> Department:
    return select_general(Department)

def select_course() -> Course:
    return select_general(Course)

def select_section() -> Section:
    return select_general(Section)

def select_student() -> Student:
    return select_general(Student)

def select_major() -> Major:
    return select_general(Major)

def select_student_major() -> StudentMajor:
    return select_general(StudentMajor)

def prompt_for_enum(prompt: str, cls, attribute_name: str):
    """
    :param prompt:          A text string telling the user what they are being prompted for.
    :param cls:             The class (not just the name) of the MongoEngine class that the
                            enumerated attribute belongs to.
    :param attribute_name:  The NAME of the attribute that you want a value for.
    :return:                The enum class member that the user selected.
    """
    attr = getattr(cls, attribute_name)  # Get the enumerated attribute.
    if type(attr).__name__ == 'EnumField':  # Make sure that it is an enumeration.
        enum_values = []
        for choice in attr.choices:  # Build a menu option for each of the enum instances.
            enum_values.append(Option(choice.value, choice))
        # Build an "on the fly" menu and prompt the user for which option they want.
        return Menu('Enum Menu', prompt, enum_values).menu_prompt()
    else:
        raise ValueError(f'This attribute is not an enum: {attribute_name}')

# -------------------- ADD FUNCTIONS --------------------

def add_department():
    """
    Create a new Department instance.
    :return: None
    """
    success: bool = False
    new_department = None
    while not success:
        abbreviation = input('Enter department abbreviation: ')
        name = input('Enter department name: ')
        chair_name = input('Enter chair name: ')
        building = input('Enter building: ')
        office = int(input('Enter office number: '))
        description = input('Enter description: ')
        new_department = Department(
            abbreviation,
            name,
            chair_name,
            building,
            office,
            description
        )
        violated_constraints = unique_general(new_department)
        if len(violated_constraints) > 0:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('try again')
        else:
            try:
                print("Work")
                new_department.save()
                success = True
            except Exception as e:
                print('Errors adding the department:')
                Utilities.print_exception(e)

def add_course():
    """
    Create a new Course instance.
    :return: None
    """
    print("Which department offers this course?")
    department = select_department()  # You need to implement select_department function
    description = input('Please enter the course description-->')
    units = int(input('How many units for this course-->'))
    success: bool = False
    new_course = None
    while not success:
        name = input("Course full name--> ")
        number = int(input("Course number--> "))
        new_course = Course(department, number, name, description, units)
        violated_constraints = unique_general(new_course)
        if len(violated_constraints) > 0:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('try again')
        else:
            try:
                new_course.save()
                success = True
            except Exception as e:
                print('Errors adding the course:')
                Utilities.print_exception(e)

def add_section():
    """
    Create a new Section instance.
    :return: None
    """
    print("Which course offers this section?")
    course = select_course()
    success: bool = False
    new_section = None
    while not success:
        section_number = int(input('Please enter the section number->'))
        semester = input("semester--> ")
        year = int(input("Course year--> "))
        building = input("building--> ")
        room = int(input("room number--> "))
        schedule = input("schedule--> ")
        hour = int(input("Hour--> "))
        minute = int(input("Minute--> "))
        second = int(input("Second--> "))
        start_time = str(hour) + ":" + str(minute) + ":" + str(second)
        instructor = input("instructor--> ")
        new_section = Section(course, section_number, semester, year,
                          building, room, schedule, start_time,
                          instructor)
        violated_constraints = unique_general(new_section)
        if len(violated_constraints) > 0:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('try again')
        else:
            try:
                new_section.save()
                success = True
            except Exception as e:
                print('Errors adding the section:')
                Utilities.print_exception(e)

def add_student():
    """
    Create a new Student instance.
    :return: None
    """
    success: bool = False
    new_student = None
    while not success:
        last_name = input("Student last name--> ")
        first_name = input("Student first name-->")
        email = input("Student e-mail address--> ")
        new_student = Student(last_name, first_name, email)
        violated_constraints = unique_general(new_student)
        if len(violated_constraints) > 0:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('try again')
        else:
            try:
                new_student.save()
                success = True
            except Exception as e:
                print('Errors adding the student:')
                Utilities.print_exception(e)

def add_major():
    """
    Create a new Major instance.
    :return: None
    """
    success: bool = False
    new_major = None
    while not success:
        name = input("Major name--> ")
        description = input('Please give this major a description -->')
        new_major = Major(name, description)
        violated_constraints = unique_general(new_major)
        if len(violated_constraints) > 0:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('try again')
        else:
            try:
                new_major.save()
                success = True
            except Exception as e:
                print('Errors adding the major:')
                Utilities.print_exception(e)

def add_student_major():
    success: bool = False
    new_student_major = None
    while not success:
        student = select_student()
        major = select_major()
        # year = int(input('Enter a year'))
        # month = int(input('Enter a month'))
        # day = int(input('Enter a day'))
        decDate = prompt_for_date("Enter date: ")
        new_student_major = StudentMajor(student, major, decDate)
        violated_constraints = unique_general(new_student_major)
        if len(violated_constraints) > 0:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('try again')
        else:
            try:
                new_student_major.save()
                success = True
            except Exception as e:
                print('Errors adding the student major:')
                Utilities.print_exception(e)

# ------------------ DELETE FUNCTIONS ---------------------

def delete_department():
    """
    Delete an existing department from the database.
    :return: None
    """
    department = select_department()
    majors = department.majors
    for major in majors:
        majors.delete()
    # Now that all the items on the order are removed, we can safely remove the order itself.
    department.delete()

def delete_course():
    """
    Delete an existing course from the database.
    :return: None
    """
    course = select_course()
    sections = course.sections
    for section in sections:
        section.delete()
    # Now that all the items on the order are removed, we can safely remove the order itself.
    course.delete()

def delete_section():
    """
    Delete an existing section from the database.
    :return: None
    """
    section = select_section()
    # sections = course.sections
    # for section in sections:
    #     section.delete()
    # Now that all the items on the order are removed, we can safely remove the order itself.
    section.delete()

def delete_student():
    """
    Delete an existing student from the database.
    :return: None
    """
    student = select_student()
    studentMajors = student.studentMajors
    for major in studentMajors:
        major.delete()
    # Now that all the items on the order are removed, we can safely remove the order itself.
    student.delete()

def delete_major():
    """
    Delete an existing major from the database.
    :return: None
    """
    major = select_major()
    major.delete()

def delete_student_major():
    """
    Delete an existing major from the database.
    :return: None
    """
    studentMajor = select_student_major()
    studentMajor.delete()

# --------------------- LIST FUNCTIONS ------------------------

def list_departments():
    departments = Department.objects.all()
    for department in departments:
        print(department)
        print("------------------------")

def list_courses():
    courses = Course.objects.all()
    for course in courses:
        print(course)
        print("------------------------")

def list_sections():
    sections = Section.objects.all()
    for section in sections:
        print(section)
        print("------------------------")

def list_students():
    students = Student.objects.all()
    for student in students:
        print(student)
        print("------------------------")

def list_majors():
    majors = Major.objects.all()
    for major in majors:
        print(major)
        print("------------------------")

def list_student_majors():
    studentMajors = StudentMajor.objects.all()
    for x in studentMajors:
        print(x)
        print("------------------------")

if __name__ == '__main__':
    print('Starting in main.')
    monitoring.register(CommandLogger())
    db = Utilities.startup()
    main_action: str = ''
    while main_action != menu_main.last_action():
        main_action = menu_main.menu_prompt()
        print('next action: ', main_action)
        exec(main_action)
    log.info('All done for now.')
