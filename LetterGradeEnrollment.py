from mongoengine import *
from Enrollment import Enrollment

class LetterGrade(Enrollment):
    '''
    Create class documentation here for later
    '''
    minSatisfactory = StringField(db_field='min_satisfactory_grade', required=True)

    def __str__(self):
        result = f'''Enrollment:
                     {self.student.firstName} {self.student.lastName}
                     {self.section.course.courseName} {self.section.course.courseNumber}- {self.section.sectionNumber}
                     Type - Letter Grade \n'''
        return result
