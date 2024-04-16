from ConstraintUtilities import select_general, unique_general, prompt_for_date
from Utilities import Utilities
from CommandLogger import CommandLogger, log
from pymongo import monitoring
from mongoengine import *
from Menu import Menu
from Option import Option
from menu_definitions import menu_main, add_select, list_select, select_select, delete_select, update_select
from Department import Department
from Course import Course
from Section import Section

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

def select():
    menu_loop(select_select)

def delete():
    menu_loop(delete_select)

def update():
    menu_loop(update_select)

def select_department() -> Department:
    return select_general(Department)

def select_course() -> Course:
    return select_general(Course)

def select_section() -> Section:
    return select_general(Section)

def add_department():
    """
    Create a new Department instance
    """
    success: bool = False
    new_department = None
    while not success:
        new_department = Department(
            name = input('Name --> '),
            abbreviation = input('Abbreviation --> '),
            chairName = input('Chair Name --> '),
            building = input('Building --> '),
            office = int(input('Office --> ')),
            description = input('Description --> ')
        )
        violated_constraints = unique_general(new_department)
        if len(violated_constraints) > 0:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('try again')
        else:
            try:
                new_department.save()
                success = True
                print('Successfully added a new department!')
            except Exception as e:
                print('Errors adding new department!')
                print(Utilities.print_exception(e))

def add_course():
    """
    Create a new Course instance within a Department
    """
    success: bool = False
    new_course = None
    department = select_department()
    print(department)
    while not success:
        new_course = Course(
            department = department,
            courseName = input('Course Name --> '),
            courseNumber = int(input('Course Number --> ')),
            description = input('Description --> '),
            units = int(input('Units --> '))
        )
        print('Created a new course instance!')
        violated_constraints = unique_general(new_course)
        if len(violated_constraints) > 0:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('try again')
        else:
            try:
                new_course.save()
                department.courses.append(new_course)
                department.save()
                success = True
                print('Successfully added a new course!')
            except Exception as e:
                print('-- Errors adding new course! --')
                print(Utilities.print_exception(e))

def add_section():
    """
    Create a new Section instance within a Course
    """
    success: bool = False
    course = select_course()
    print(course)
    while not success:
        new_section= Section(
            sectionNumber = int(input('Section Number --> ')),
            semester = input('Semester --> '), 
            sectionYear = int(input('Year --> ')),
            building = input('Building --> '),
            room = int(input('Room --> ')),
            schedule = input('Schedule --> '),
            startTime = prompt_for_date('Date and Time For Section'),
            instructor = input('Instructor --> '),
            course = course
        )
        print('Created a new section instance!')
        violated_constraints = unique_general(new_section)
        if len(violated_constraints) > 0:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('try again')
        else:
            try:
                new_section.save()
                course.sections.append(new_section)
                course.save()
                success = True
                print('Successfully added a new section!')
            except Exception as e:
                print('-- Errors adding new section! --')
                print(Utilities.print_exception(e))

def list_department():
    """
    Prints an instance of a department
    """
    department: Department
    department = select_department()
    print(department)

def list_course():
    """
    Prints an instance of a course
    """
    course: Course
    course = select_course()
    print(course)

def list_section():
    """
    Prints an instance of a section
    """
    section: Section
    section = select_section()
    print(section)

def delete_department():
    """
    Delete an existing department from the database.
    :return: None
    """
    department = select_department()  # prompt the user for a department to delete
    courses = department.courses
    for course in courses:
        """
        Checks to see if there are courses under this department and if there are
        delete the courses before deleting the department
        """
        print('-- WARNING: The following course is in the department! --')
        print('-- Must delete all courses in a department before you can delete the department')
        print(course)
        print('Would you like to delete this course ?\n1 - Yes\n0 - No')
        course_continue = int(input('--> '))
        if course_continue == 1:
            sections = course.sections
            for section in sections:
                """
                Checks to see if there are sections in each of the courses, if there are then
                delete the sections from the course
                """
                print('-- WARNING: The following section is in the course! --')
                print('-- Must delete all sections in a course before you can delete the course')
                print(section)
                print('Would you like to delete this section ?\n1 - Yes\n0 - No')
                section_continue = int(input('--> '))
                if section_continue == 1:
                    section.delete()
                    print('-- Successfully deleted section --')
                else: return
            course.delete()
            print('-- Successfully deleted course --')
        else: return
    # delete the department once it is emptied of its courses
    department.delete()
    print('-- Successfully deleted department --')

def delete_course():
    """
    Delete an existing course from a database
    :return: None
    """
    course = select_course()  # prompt the user for a course to delete
    sections = course.sections
    for section in sections:
        """
        Checks to see if there are sections under this course and if there are
        delete the sections before deleting the course
        """
        print('-- WARNING: The following section is in the course! --')
        print('-- Must delete all sections in a course before you can delete the course')
        print(section)
        print('Would you like to delete this section ?\n1 - Yes\n0 - No')
        section_continue = int(input('--> '))
        if section_continue == 1:
            section.delete()
            print('-- Successfully deleted section --')
        else: return
    # delete the course once it is emptied of its courses
    course.delete()

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
