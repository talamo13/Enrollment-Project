from mongoengine import *
from Enrollment import Enrollment

class LetterGrade(Enrollment):
    '''
    Create class documentation here for later
    '''
    minSatisfactory = StringField(db_field='min_satisfactory_grade', required=True)
