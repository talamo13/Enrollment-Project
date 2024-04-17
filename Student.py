from mongoengine import *

# need to add deletion functionality to this class via main.py
class Student(Document):
    """
    Create documentation for this class here
    """
    firstName = StringField(db_field='first_name', required=True)
    lastName = StringField(db_field='last_name', required=True)
    email = StringField(db_field='email', required=True)

    meta = {'collection': 'students',
            'indexes': [
            {'unique':True, 'fields':['firstName', 'lastName'], 'name': 'students_pk'}
            ]}

    def __str__(self):
        result = f'''Student:
                    {self.firstName} {self.lastName}
                    {self.email}\n'''
        return result
