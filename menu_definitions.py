from Menu import Menu
import logging
from Option import Option

menu_logging = Menu('debug', 'Please select the logging level from the following:', [
    Option("Debugging", "logging.DEBUG"),
    Option("Informational", "logging.INFO"),
    Option("Error", "logging.ERROR")
])

menu_main = Menu('main', 'Please select one of the following options:', [
    Option("Add new instance", "add()"),
    Option("Delete existing instance", "delete()"),
    Option("List existing instances", "list_members()"),
    Option("Exit", "pass")
])

# options for adding a new instance
add_select = Menu('add select', 'Which type of object do you want to add?:', [
    Option("Departments", "add_department()"),
    Option("Courses", "add_course()"),
    Option("Sections", "add_section()"),
    Option("Students", "add_student()"),
    Option("Majors", "add_major()"),
    Option("Student Majors", "add_student_major()"),
    Option("Exit", "pass")
])

# options for deleting an existing instance
delete_select = Menu('delete select', 'Which type of object do you want to delete?:', [
    Option("Departments", "delete_department()"),
    Option("Courses", "delete_course()"),
    Option("Sections", "delete_section()"),
    Option("Students", "delete_student()"),
    Option("Majors", "delete_major()"),
    Option("Student Majors", "delete_student_major()"),
    Option("Exit", "pass")
])

# options for listing the existing instances
list_select = Menu('list select', 'Which type of object do you want to list?:', [
    Option("Departments", "list_departments()"),
    Option("Courses", "list_courses()"),
    Option("Sections", "list_sections()"),
    Option("Students", "list_students()"),
    Option("Majors", "list_majors()"),
    Option("Student Majors", "list_student_majors()"),
    Option("Exit", "pass")
])
