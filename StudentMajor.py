from mongoengine import *
from Student import Student
from Major import Major

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
