import datetime

from django.core.validators import MinValueValidator, MaxValueValidator

from lessons.models import Course, LessonPlan
from schedules.managers import *
from schoolyears.constants import JUNIOR_HIGH_SCHOOL


class SchoolPeriodType(models.Model):
    school = models.ForeignKey('schoolyears.School')
    period_name = models.CharField(max_length=64)
    objects = SchoolPeriodTypeManager()
    # created_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    period_type = models.CharField(
        max_length=32,
        choices=PERIOD_TYPES,
        default=PERIOD_TYPE_NORMAL,
    )

    def get_period_type_color(self):
        return PERIOD_TYPE_COLORS[self.period_type]

    def get_period_type_text(self):
        for item in PERIOD_TYPES:
            if self.period_type == item[0]:
                return item[1]
        return None

    def __str__(self):
        return self.period_name

class SchoolPeriod(models.Model):
    school_period_type = models.ForeignKey(SchoolPeriodType)
    period_number = models.SmallIntegerField()
    start_time = models.TimeField(default=datetime.time(0, 0))
    end_time = models.TimeField(default=datetime.time(0, 0))
    objects = SchoolPeriodManager()
    # created_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return " | ".join([self.school_period_type.school.name,
                           self.school_period_type.period_name,
                           str(self.period_number),
                           str(self.start_time),
                           str(self.end_time)])

class SchoolSection(models.Model):
    school = models.ForeignKey('schoolyears.School')
    year_level = models.SmallIntegerField(default=1)
    section_count = models.SmallIntegerField(default=4, validators=[MinValueValidator(1), MaxValueValidator(10)])
    objects = SchoolSectionManager()
    is_special_needs = models.BooleanField(default=False)
    # created_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    def get_finished_activities_of_each_section(self):   
        sections = Section.objects.filter(school_section=self).order_by('section_name')
        for section in sections:
            section.classes = section.get_finished_activities_of_a_section(limit=5)
        return sections

    # Call this method once the new section_count has been updated
    def update_section_count_info(self):
        sections = Section.objects.filter(school_section=self)
        section_count = sections.count()

        if self.section_count >= 0:
            if section_count > self.section_count:
                while section_count > self.section_count:
                    section_to_delete = Section.objects.filter(
                        school_section=self, 
                        section_name=str(section_count)
                    )
                    section_to_delete.delete()
                    section_count -= 1

            elif section_count < self.section_count:
                while section_count < self.section_count:
                    section_count += 1
                    if self.school.school_type == JUNIOR_HIGH_SCHOOL:
                        new_section = chr(64+section_count)
                    else:
                        new_section = str(section_count)
                    section_to_add = Section(
                        school_section=self,
                        section_name=str(new_section),
                        teacher_name='',
                        notes=''
                    )
                    section_to_add.save()

    def set_total_students(self):
        sections = Section.objects.filter(school_section=self)
        self.total_students = 0
        if sections.count() > 0:
            for section in sections:
                self.total_students += section.student_count

    def __str__(self):
        return " | ".join([self.school.name,
                           str(self.year_level),
                           str(self.section_count)])

class SchoolSectionCourse(models.Model):
    school_section = models.ForeignKey(SchoolSection)
    course = models.ForeignKey(Course)
    # created_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return ' || '.join([str(self.id), str(self.school_section), str(self.course)])

class Section(models.Model):
    school_section = models.ForeignKey(SchoolSection)
    section_name = models.CharField(max_length=16)
    teacher_name = models.CharField(max_length=64, blank=True)
    notes = models.TextField(blank=True)
    student_count = models.SmallIntegerField(default=30)
    # created_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    def get_finished_activities_of_a_section(self, limit=None):
        count = SectionPeriod.objects.filter(section=self).count()
        query = SectionPeriod.objects.filter(section=self, date__lte=datetime.datetime.now()).order_by('-date')
        if limit is not None:
            query = query[:limit]            
        return {'count': count, 'all_classes': query}

    def __str__(self):
        return " | ".join([self.school_section.school.name,
                           self.section_name,
                           self.teacher_name])

class SectionPeriod(models.Model):
    date = models.DateField()
    section = models.ForeignKey(Section)
    school_period = models.ForeignKey(SchoolPeriod)
    lesson_plan = models.ForeignKey(LessonPlan)
    lesson_number = models.SmallIntegerField()
    hour_number = models.SmallIntegerField()
    notes = models.TextField(blank=True, null=True)
    objects = SectionPeriodManager()
    # created_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return " || ".join([str(self.date)])

class SectionPeriodType(models.Model):
    date = models.DateField()
    school = models.ForeignKey('schoolyears.School')
    school_period_type = models.ForeignKey(SchoolPeriodType)
    # created_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return " | ".join([str(self.date), self.school_period_type.period_name])
