from mongoengine import*

class Section(Document):
    """
    Create documentation for this class here
    """
    sectionNumber = IntField(db_field='section_number', min_value=0, required=True)
    semester = StringField(db_field='semester', required=True)
    sectionYear = IntField(db_field='section_year', required=True)
    building = StringField(db_field='building', required=True)
    room = IntField(db_field='room', min_value=0, required=True)
    schedule = StringField(db_field='schedule', required=True)
    startTime = DateTimeField(db_field='start_time', required=True)
    instructor = StringField(db_field='instructor', required=True)
    course = ReferenceField(Course, required=True, reverse_delete_rule=mongoengine.DENY)

    meta = {'collection': 'sections',
            'indexes': [
                {'unique': True, 'fields': ['section_number'], 'name': 'sections_pk'},
            ]}
