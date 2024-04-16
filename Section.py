import mongoengine
from mongoengine import*
from Course import Course

class Section(Document):
    """
    Create documentation for this class here
    """
    sectionNumber = IntField(db_field='section_number', min_value=0, required=True)
    semester = StringField(db_field='semester', required=True)
    sectionYear = IntField(db_field='section_year', required=True)
    building = StringField(db_field='building', required=True)
    room = IntField(db_field='room', min_value=0, required=True)
    schedule = StringField(db_field='schedule', required=True) # Maybe change this to enumeration? 
    startTime = DateTimeField(db_field='start_time', required=True) # This may need to be changed
    instructor = StringField(db_field='instructor', required=True)
    course = ReferenceField(Course, required=True, reverse_delete_rule=mongoengine.DENY)

    meta = {'collection': 'sections',
            'indexes': [
                {'unique': True, 'fields': ['course','sectionNumber'], 'name': 'sections_pk'}
            ]}

    def __str__(self):
        result = f'''Section:
                    Number - {self.sectionNumber}
                    {self.sectionYear} {self.semester}
                    {self.building} {self.room}
                    {self.schedule} {self.startTime}
                    {self.course.courseName} - {self.instructor}'''
        return result
