from django.core.management.base import BaseCommand, CommandError
from schoolyears.models import *
from schedules.models import *
from lessons.models import *
from datetime import datetime, timedelta
from schoolyears.constants import BLUE, GREEN, ELEMENTARY_SCHOOL, JUNIOR_HIGH_SCHOOL

class Command(BaseCommand):
    help = 'Resets the relevant tables of the database'

    def __add_school(self, school_colors, school_type, school_year, name, name_kanji, address, contact_number, website, principal, vice_principal, english_head_teacher):
        new_school = School(
            school_colors=school_colors,
            school_type=school_type,
            school_year=school_year,
            name=name,
            name_kanji=name_kanji,
            address=address,
            contact_number=contact_number,
            website=website,
            principal=principal,
            vice_principal=vice_principal,
            english_head_teacher=english_head_teacher,
        )
        new_school.save()
        return new_school

    def __add_yearly_schedule(self, school_year, school, date):
        schedule = YearlySchedule(
            school_year=school_year,
            school=school,
            date=date,
        )
        schedule.save()

    def __add_null_lesson_plan(self):
        new_lsp = LessonPlan(
            greeting=None,
            warmup=None,
            presentation=None,
            practice=None,
            production=None,
            cooldown=None,
            assessment=None,
        )
        new_lsp.save()
        return new_lsp

    def __add_scheduled_class(self, school, date, year_level, period_number, section_name):
        year_level = SchoolSection.objects.get(school=school, year_level=year_level)

        if school.school_type == ELEMENTARY_SCHOOL:
            weekday = date.weekday() # 0 is Monday, 6 is Saturday
            period_type = PERIOD_TYPE_NORMAL
            if weekday == 0:
                period_type = PERIOD_TYPE_MONDAY
            elif weekday == 2:
                period_type = PERIOD_TYPE_WEDNESDAY
        else:
            period_type = PERIOD_TYPE_NORMAL

        school_period = SchoolPeriod.objects.get(
            period_number=period_number, 
            school_period_type=SchoolPeriodType.objects.get(school=school, period_type=period_type))

        new_section_period = SectionPeriod(
            date=date,
            section=Section.objects.get(school_section=year_level, section_name=section_name),
            school_period=school_period,
            lesson_plan=self.__add_null_lesson_plan(),
            lesson_number=1,
            hour_number=1,
        )
        new_section_period.save()

    def handle(self, *args, **options):
        # Delete all relevant tables
        SchoolPeriodType.objects.all().delete()
        SchoolPeriod.objects.all().delete()
        SchoolSection.objects.all().delete()
        SchoolSectionCourse.objects.all().delete()
        Section.objects.all().delete()
        SectionPeriod.objects.all().delete()
        SectionPeriodType.objects.all().delete()

        RouteInfo.objects.all().delete()
        Path.objects.all().delete()
        Node.objects.all().delete()
        SpecialYearlySchedule.objects.all().delete()
        YearlySchedule.objects.all().delete()
        SchoolRoute.objects.all().delete()
        SchoolYear.objects.all().delete()
        School.objects.all().delete()

        # Add a school year from Apr 1 of this year, to Mar 30 of next year
        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        current_year = datetime.now().year
        next_year = current_year + 1
        start_date = datetime.strptime(('%d-04-01')%(current_year), '%Y-%m-%d')
        end_date = datetime.strptime(('%d-03-30')%(next_year), '%Y-%m-%d')
        new_school_year = SchoolYear(
            name = '%d ~ %d'%(current_year, next_year),
            start_date = start_date,
            end_date = end_date,
            is_active = True
        )
        new_school_year.save()

        # Add two schools: Dolphin ES and Shark JHS
        dolphin_es = self.__add_school(
            school_colors=BLUE,
            school_type=ELEMENTARY_SCHOOL,
            school_year=new_school_year,
            name='Dolphin Elementary',
            name_kanji='イルカ小学校',
            address='123-4567 Tursiops Road, Artiodactyla City, Mammalia',
            contact_number='050-1234-5678',
            website='N/A',
            principal='Iruyo',
            vice_principal='Inaiyo',
            english_head_teacher='Ikuyo',
        )
        shark_jhs = self.__add_school(
            school_colors=GREEN,
            school_type=JUNIOR_HIGH_SCHOOL,
            school_year=new_school_year,
            name='Shark Junior High',
            name_kanji='鮫中学校',
            address='987-6543 Galeocerdo Road, Chondrichthyes City, Carcharhiniformes',
            contact_number='060-9876-5432',
            website='N/A',
            principal='Ripster',
            vice_principal='Streex',
            english_head_teacher='Slammu',
        )

        self.__add_yearly_schedule(new_school_year, dolphin_es, today)
        self.__add_yearly_schedule(new_school_year, shark_jhs, tomorrow)

        self.__add_scheduled_class(
            school=dolphin_es,
            date=today, 
            year_level=3, 
            period_number=1, 
            section_name='1')
        self.__add_scheduled_class(
            school=dolphin_es,
            date=today, 
            year_level=3, 
            period_number=2, 
            section_name='2')

        self.__add_scheduled_class(
            school=shark_jhs,
            date=tomorrow, 
            year_level=2, 
            period_number=1, 
            section_name='A')
        self.__add_scheduled_class(
            school=shark_jhs,
            date=tomorrow, 
            year_level=2, 
            period_number=2, 
            section_name='B')

        self.stdout.write(self.style.SUCCESS('Database resetting has started.'))