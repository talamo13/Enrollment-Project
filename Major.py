from mongoengine import *

class Major(Document):
    """
    Documentation for this class will go here
    """
    name = StringField(db_field='name', required='True')
    description = StringField(db_field='description', required=True)

    meta = {'collection': 'majors',
            'indexes': [
                {'unique': True, 'fields': ['name'], 'name': 'majors_pk_01'}
            ]}

    def __str__(self):
        result = f'''Major:
                    {self.name}
                    {self.description}'''
        return result
