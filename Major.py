import mongoengine
from mongoengine import *
from Department import Department

class Major(Document):
    """
    Documentation for this class will go here
    """
    name = StringField(db_field='name', required='True')
    description = StringField(db_field='description', required=True)
    department = ReferenceField(Department, required=True, reverse_delete_rule=mongoengine.DENY)

    meta = {'collection': 'majors',
            'indexes': [
                {'unique': True, 'fields': ['name'], 'name': 'majors_uk_01'}
            ]}

    def __init__(self, name, description, department, *args, **values):
        super().__init__(*args, **values)
        self.name = name
        self.description = description
        self.department = department

    def __str__(self):
        result = f'''Major:
                    {self.name}
                    {self.description}'''
        return result
