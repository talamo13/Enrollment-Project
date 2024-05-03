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
from Student import Student
from Enrollment import Enrollment
from PassFailEnrollment import PassFail
from LetterGradeEnrollment import LetterGrade
from Major import Major
from StudentMajor import StudentMajor

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

def select_student() -> Student:
    return select_general(Student)

def select_enrollment() -> Enrollment:
    return select_general(Enrollment)

def select_major() -> Major:
    return select_general(Major)

def select_student_major() -> StudentMajor:
    return select_general(StudentMajor)

def choose_building():
    """
    Prompts the user to select from a list of buildings on campus.
    This enforces the business rule of only certain building being allowed to be assigned to a department.
    """
    choice = 0
    buildings = {1:'ANAC',2:'CDC',3:'DC',4:'ECS',5:'EN2',6:'EN3',7:'EN4',8:'EN5',9:'ET',10:'HSCI',11:'NUR',12:'VEC'};
    while choice not in {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}:
        print("Select A Building:\n1 - ANAC\n2 - CDC\n3 - DC\n4 - ECS\n5 - EN2\n6 - EN3\n7 - EN4\n8 - EN5\n9 - ET\n10 - HSCI\n11 - NUR\n12 - VEC")
        choice = int(input('--> ')) 
    return buildings[choice]

def choose_schedule():
    """
    Prompts the user to select from a list of possible schedule choices. 
    This enforces the business rule of their only being specific options for schedules
    """
    choice = 0
    schedules = {1:'MW',2:'TuTh',3:'MWF',4:'F',5:'S'}
    while choice not in {1, 2, 3, 4, 5}:
        print("Select A Schedule:\n1 - MW\n2 - TuTh\n3 - MWF\n4 - F\n5 - S")
        choice = int(input('--> '))
    return schedules[choice]

def choose_semester():
    """
    Prompts the user to select from a list of possible semesters.
    This enforces the business rule of there only being certain semesters that the user can choose from
    """
    choice = 0
    semesters = {1:'Fall',2:'Spring',3:'Summer I',4:'Summer II',5:'Summer III',6:'Winter'}
    while choice not in {1, 2, 3, 4, 5, 6}:
        print("Select A Semester:\n1 - Fall\n2 - Spring\n3 - Summer I\n4 - Summer II\n5 - Summer III\n6 - Winter")
        choice = int(input('--> '))
    return semesters[choice]

def choose_grade():
    """
    Prompts the user to select their minimum satisfactory grade from a list of valid values.
    This enforces the business rule that the minimum satisfactory grade is a list of certain values.
    """
    choice = 0
    grades = {1:'A',2:'B',3:'C'}
    while choice not in {1,2,3}:
        print('Select A Minimum Satisfactory Grade:\n1 - A\n2 - B\n3 - C')
        choice = int(input('--> '))
    return grades[choice]

def choose_enrollment():
    """
    Prompts the user to choose wether the enrollment they are making is of type PassFail or LetterGrade
    """
    choice = 0
    enrollment_types = {1:'Pass Fail',2:'Letter Grade'}
    while choice not in {1,2,3}:
        print('Select An Enrollment Type:\n1 - Pass Fail\n2 - Letter Grade')
        choice = int(input('--> '))
    return enrollment_types[choice] 

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
            building = choose_building(),
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
            departmentAbbreviation = department.abbreviation,
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
            sectionYear = int(input('Year --> ')),
            semester = choose_semester(), 
            sectionNumber = int(input('Section Number --> ')),
            instructor = input('Instructor --> '),
            building = choose_building(),
            room = int(input('Room --> ')),
            schedule = choose_schedule(),
            startTime = prompt_for_date('Start Time:'),
            course = course,
            courseNumber = course.courseNumber,
            departmentAbbreviation = course.department.abbreviation
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

def add_student():
    """
    Create a new Student instance
    """
    success: bool = False
    while not success:
        new_student = Student(
            firstName = input('First name --> '), 
            lastName = input('Last name --> '),
            email = input('Email --> ')
        )
        print('Created a new student instance!')
        violated_constraints = unique_general(new_student)
        if len(violated_constraints) > 0:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('try again')
        else:
            try:
                new_student.save()
                success = True
                print('Successfully added a new section!')
            except Exception as e:
                print('-- Errors adding new section! --')
                print(Utilities.print_exception(e))

def add_enrollment():
    """
    Create a new Enrollment instance
    """
    student = select_student()
    section = select_section()
    enrollment_type = choose_enrollment()
    if enrollment_type == 'Pass Fail':
        add_pass_fail(student, section)
    else:
        add_letter_grade(student, section)

def add_pass_fail(student, section):
    """
    Create a new PassFail enrollment instance
    """
    success: bool = False 
    while not success:
        new_enrollment = PassFail(
            applicationDate = prompt_for_date('Application Date:'),
            student = student,
            section = section
        )
        print('Created a new enrollment instance!')
        violated_constraints = unique_general(new_enrollment)
        if len(violated_constraints) > 0:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('try again')
        else:
            try:
                new_enrollment.save()
                success = True
                print('Successfully added a new enrollment!')
            except Exception as e:
                print('-- Errors adding new section! --')
                print(Utilities.print_exception(e))

def add_letter_grade(student, section):
    """
    Create a new LetterGrade enrollment instance
    """
    success: bool = False 
    while not success:
        new_enrollment = LetterGrade(
            minSatisfactory = choose_grade(),
            student = student,
            section = section
        )
        print('Created a new enrollment instance!')
        violated_constraints = unique_general(new_enrollment)
        if len(violated_constraints) > 0:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('try again')
        else:
            try:
                new_enrollment.save()
                success = True
                print('Successfully added a new enrollment!')
            except Exception as e:
                print('-- Errors adding new section! --')
                print(Utilities.print_exception(e))

def add_major():
    """
    Create a new Major instance
    """
    success: bool = False
    department = select_department()
    while not success:
        new_major = Major(
            department = department,
            name = input('Major name --> '),
            description = input('Description --> ')
        )
        print('Created a new major instance!')
        violated_constraints = unique_general(new_major)
        if len(violated_constraints) > 0:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('try again')
        else:
            try:
                new_major.save()
                department.majors.append(new_major)
                department.save()
                success = True
                print('Successfully added a new major!')
            except Exception as e:
                print('-- Errors adding new section! --')
                print(Utilities.print_exception(e))

def add_student_major():
    """
    Create a new StudentMajor instance
    """
    success: bool = False
    student = select_student()
    major = select_major()
    while not success:
        new_student_major = StudentMajor(
            student = student, 
            major = major,
            declarationDate = prompt_for_date('Declaration Date:') 
        )
        print('Created a new major instance!')
        violated_constraints = unique_general(new_student_major)
        if len(violated_constraints) > 0:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('try again')
        else:
            try:
                new_student_major.save()
                success = True
                print('Successfully added a new student major!')
            except Exception as e:
                print('-- Errors adding new student major! --')
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

def list_student():
    """
    Prints an instance of a student
    """
    student: Student
    student = select_student()
    print(student)

def list_enrollment():
    """
    Prints an instance of an enrollment
    """
    enrollment: Enrollment
    enrollment = select_enrollment()
    print(enrollment)

def list_major():
    """
    Prints an instance of a major
    """
    major: Major
    major = select_major()
    print(major)

def list_student_major():
    """
    Prints an instance of student major
    """
    student_major: StudentMajor
    student_major = select_student_major()
    print (student_major)

def delete_department():
    """
    Delete an existing department from the database.
    :return: None
    """
    department = select_department()  # prompt the user for a department to delete
    courses = department.courses
    majors = department.majors
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
            delete_course(course)
        else: return
    for major in majors:
        """
        Checks to see if there are majors under this department and if there are
        delete the majors before deleting the department
        """
        print('-- WARNING: The following major is in the department! --')
        print('-- Must delete all major in a department before you can delete the department')
        print(course)
        print('Would you like to delete this major ?\n1 - Yes\n0 - No')
        major_continue = int(input('--> '))
        if major_continue == 1:
            delete_major(major)
        else: return
    # delete the department once it is emptied of its courses
    department.delete()
    print('-- Successfully deleted department --')

def delete_course_main():
    """
    Acts as a bridge funciton to delete_course
    """
    course = select_course()
    delete_course(course)

def delete_course(course):
    """
    Delete an existing course from a database
    :return: None
    """
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
            delete_section(section)
            print('-- Successfully deleted section --')
        else: return
    # delete the course once it is emptied of its courses
    course.delete()

def delete_section_main():
    """
    Bridge function for delte_section()
    """
    section = select_section()
    delete_section(section)

def delete_section(section):
    """
    Delete an existing section from the database
    :returns: None
    """
    enrollments = Enrollment.objects(section = section)
    for enrollment in enrollments:
        print('-- WARNING: The following enrollment is in this section! --') 
        print('-- Must delete all enrollments in section before you can delete the course')
        print(enrollment)
        print('Would you like to delete the enrollment ?\n1 - Yes\n0 - No')
        enrollment_continue = int(input('--> '))
        if enrollment_continue == 1:
            delete_enrollment(enrollment)
        else: return
    course = Course.objects(sections = section)
    course.update(pull__sections=section.id) # delete this section from the Course.sections list
    section.delete() # delete section once all the enrollments have been deleted

def delete_enrollment_main():
    """
    Bridge function for delete_enrollment()
    """
    enrollment = select_enrollment()
    delete_enrollment(enrollment)

def delete_enrollment(enrollment):
    """
    Deletes an existing enrollment from the database
    """
    enrollment.delete()
    print('Enrollment successfully deleted!')

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
