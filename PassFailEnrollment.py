from mongoengine import *
from Enrollment import Enrollment
from datetime import datetime, date

class PassFail(Enrollment):
    '''
    Create class documentation here for later
    '''
    applicationDate = DateTimeField(db_field='application_date', required=True)

    def clean(self):
        """
        clean() is called within save(), so this will automatically be called whenever trying to save an instance of Section
        Using this function to enforce the business rule that declarationDate <= today
        """
        today = datetime.now()
        if not (self.applicationDate <= today):
            raise ValidationError('Application date must not be in the future!')

    def __str__(self):
        result = f'''Enrollment:
                     {self.student.firstName} {self.student.lastName}
                     {self.section.course.courseName} {self.section.course.courseNumber}- {self.section.sectionNumber}
                     Type - Pass / Fail \n'''
        return result
