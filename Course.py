import mongoengine
from mongoengine import *
from Department import Department

class Course(Document): 
    """
    Create documentation for this class here
    """
    # are there min and max lengths already defined in the moon model?? if so then change the max and min values
    courseNumber = IntField(db_field='course_number', min_value=100, max_value=699, required=True)
    courseName = StringField(db_field='course_name', required=True)
    description = StringField(db_field='description', required=True)
    units = IntField(db_field='units', min_value=1, max_value=5, required=True)
    department = ReferenceField(Department, required=True, reverse_delete_rule=mongoengine.DENY)
    departmentAbbreviation = StringField(db_field='department_abbreviation', required=True)
    sections = ListField(ReferenceField('Section'))

    meta = {'collection': 'courses',
            'indexes': [
                {'unique': True, 'fields': ['departmentAbbreviation','courseNumber'], 'name': 'courses_uk_01'},
                {'unique': True, 'fields': ['departmentAbbreviation','courseName'], 'name': 'courses_uk_02'}
            ]}

    def __init__(self, number, name, description, units, department, abbr, *args, **values):
        super().__init__(*args, **values)
        if self.sections is None:
            self.sections = []
        self.courseNumber = number
        self.courseName = name
        self.description = description
        self.units = units
        self.department = department
        self.departmentAbbreviation = abbr

    def __str__(self):
        """
        Returns a string representation of a Course instance
        """
        result = f'''Course:
                    {self.courseName} - {self.courseNumber}
                    {self.description}
                    Department - {self.department.name}
                    Units - {self.units}\n'''
        return result
