from mongoengine import *

class Department(Document):
    """
    Create documentation for this class here
    """
    # are there min and max lengths already defined in the moon model?? if so then change the max and min values
    name = StringField(db_field='name', required=True)
    abbreviation = StringField(db_field='abbreviation', max_length=6)
    chairName = StringField(db_field='chair_name', max_length=60, required=True)
    building = StringField(db_field='building', required=True)
    office = IntField(db_field='office', required=True)
    description = StringField(db_field='description', max_length=80, required=True)
    courses = ListField(ReferenceField('Course'))
    majors = ListField(ReferenceField('Major'))

    meta = {'collection': 'departments',
            'indexes': [
                {'unique': True, 'fields': ['name'], 'name': 'departments_uk_01'},
                {'unique': True, 'fields': ['abbreviation'], 'name': 'departments_uk_02'},
                {'unique': True, 'fields': ['chairName'], 'name': 'departments_uk_03'}, 
                {'unique': True, 'fields': ['building', 'office'], 'name': 'departments_uk_04'}
            ]}

    def __init__(self, name, abbr, chair, building, office, description, *args, **values):
        super().__init__(*args, **values)
        if self.courses is None:
            self.courses = []
        self.name = name
        self.abbreviation = abbr
        self.chairName = chair
        self.building = building
        self.office = office
        self.description = description

    def __str__(self):
        """
        Returns a string representation of a Department instance
        """
        major_names = []
        for major in self.majors:
            major_names.append(major.name)
        course_names = []
        for course in self.courses:
            course_names.append(course.courseName)
        result = f'''\nDepartment:
                    {self.name} - {self.abbreviation}
                    Chair - {self.chairName}, {self.building} {self.office}
                    {self.description}\n
                    Majors: {major_names}\n
                    Courses: {course_names}'''
        return result

    def add_course(self, new_course):
        """
        Add a course to the list of courses offered by the department 
        """
        if self.courses:
            for course in self.courses:
                if new_course == course:
                    raise ValueError('This course already exists!')
            self.courses.append(new_course)
        else:
            self.courses = [new_course]
