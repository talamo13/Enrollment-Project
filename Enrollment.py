from mongoengine import *
from Student import Student
from Section import Section

class Enrollment(Document):
    '''
    Create class documentation here later
    '''
    student = ReferenceField(Student, db_field='student', required=True)
    section = ReferenceField(Section, db_field='section', required=True)
    departmentAbbreviation = StringField(db_field='department_abbreviation', required=True)
    semester = StringField(db_field='semester', required=True)
    sectionYear = IntField(db_field='section_year', required=True)
    courseNumber = IntField(db_field='course_number', required=True)
    
    meta = {'allow_inheritance':True,
            'collection': 'enrollments',
            'indexes': [
                {'unique': True, 'fields': ['student','section'], 'name': 'enrollments_uk_01'},
                {'unique': True, 'fields': ['departmentAbbreviation','courseNumber','student','semester','sectionYear'], 'name': 'enrollments_uk_02'}
            ]}

