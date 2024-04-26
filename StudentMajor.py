from mongoengine import *
from Student import Student
from Major import Major
import datetime

class StudentMajor(Document):
    """
    Create documentation fro this class here
    """
    student = ReferenceField(Student, db_field='student', required=True)
    major = ReferenceField(Major, db_field='major', required=True)
    declarationDate = DateTimeField(db_field='declaration_date', required=True)

    meta = {'collection': 'student_majors',
            'indexes': [
                {'unique': True, 'fields': ['student','declarationDate'], 'name': 'student_majors_pk'}
            ]}

    def __str__(self):
        result = f'''Student Major:
                    {self.student.firstName} {self.student.lastName}
                    {self.major.name}'''
        return result
    
    def clean(self):
        """
        clean() is called within save(), so this will automatically be called whenever trying to save an instance of Section
        Using this function to enforce the business rule that declarationDate <= today
        """
        today = datetime.date.today()
        if not (self.declarationDate <= today):
            raise ValidationError('Declaration date must not be in the future!')
        
