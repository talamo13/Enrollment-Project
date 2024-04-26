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
    
    #super type for becoming a super type
    # allow_inhertitance=True
    meta = {'collection': 'enrollments',
            'indexes': [
                {'unique': True, 'fields': ['student','section'], 'name': 'enrollments_pk'}
            ]}

    def __init__(self, student, section, *args, **values):
        super().__init__(*args, **values)
        self.student = student
        self.section = section

    def __str__(self):
        result = f'''Enrollment:
                     {self.student.firstName} {self.student.lastName}
                     {self.section.course.courseName} {self.section.course.courseNumber}- {self.section.sectionNumber}\n'''
        return result