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
    courseNumber = IntField(db_field='course_number', required=True)
    departmentAbbreviation = StringField(db_field='department_abbreviation', required=True)

    meta = {'collection': 'sections',
            'indexes': [
                {'unique': True,
                 'fields': ['course','sectionNumber','semester','sectionYear'],
                 'name': 'sections_uk_01'},
                {'unique': True,
                 'fields': ['semester','sectionYear','building','room','schedule','startTime'],
                 'name': 'sections_uk_02'},
                {'unique': True,
                 'fields': ['semester','sectionYear','schedule','startTime','instructor'],
                 'name': 'sections_uk_03'},
                # need to add student id ??
                {'unique': True,
                 'fields': ['semester','sectionYear','courseNumber','departmentAbbreviation'],
                 'name': 'sections_uk_04'}
            ]}

    def __init__(self, number, semester, year, building, room, schedule, startTime, instructor,
                 course, *args, **values):
        super().__init__(*args, **values)
        self. sectionNumber = number,
        self.semester = semester
        self.sectionYear = year
        self.building = building
        self.room = room
        self.schedule = schedule
        self.startTime = startTime
        self.instructor = instructor
        self.course = course
        self.courseNumber = course.courseNumber
        self.departmentAbbreviation = course.departmentAbbreviation


    def __str__(self):
        result = f'''Section:
                    Number - {self.sectionNumber}
                    {self.sectionYear} {self.semester}
                    {self.building} {self.room}
                    {self.schedule} {self.startTime}
                    {self.course.courseName} - {self.instructor}'''
        return result
