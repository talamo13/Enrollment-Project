from mongoengine import *
from Student import Student
from Section import Section


# still need to add deletion functionality to this class via main.py
class Enrollment(Document):
    '''
    Create class documentation here later
    '''
    student = ReferenceField(Student, db_field='student', required=True)
    section = ReferenceField(Section, db_field='section', required=True)

    meta = {'collection': 'enrollments',
            'indexes': [
                {'unique': True, 'fields': ['student','section'], 'name': 'enrollments_pk'}
            ]}

    def __str__(self):
        result = f'''Enrollment:
                     {self.student.firstName} {self.student.lastName}
                     {self.section.course.courseName} {self.section.course.courseNumber}- {self.section.sectionNumber}\n'''
        return result
