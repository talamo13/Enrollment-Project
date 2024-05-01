from mongoengine import *
from Student import Student
from Section import Section

class Enrollment(Document):
    '''
    Create class documentation here later
    '''
    student = ReferenceField(Student, db_field='student', required=True)
    section = ReferenceField(Section, db_field='section', required=True)
    
    meta = {'allow_inheritance':True,
            'collection': 'enrollments',
            'indexes': [
                {'unique': True, 'fields': ['student','section'], 'name': 'enrollments_pk'}
            ]}

