import json

from django.apps import apps
from django.db import models

from schedules.constants import *


class SchoolPeriodTypeManager(models.Manager):
    def __get_class_info(self, school, date):
        section_period_type_model = apps.get_model(app_label='schedules', model_name='SectionPeriodType')
        school_period_type_model = apps.get_model(app_label='schedules', model_name='SchoolPeriodType')
        school_period_model = apps.get_model(app_label='schedules', model_name='SchoolPeriod')

        section_period_type = section_period_type_model.objects.filter(school=school, date=date).first()
        school_period_type = None

        if section_period_type is None:
            # Check the day of the date. For example, if it's a Monday, use a Monday schedule
            weekday = date.weekday() # 0 is Monday, 6 is Saturday
            period_type = PERIOD_TYPE_NORMAL
            if weekday == 0:
                period_type = PERIOD_TYPE_MONDAY
            elif weekday == 2:
                period_type = PERIOD_TYPE_WEDNESDAY

            # Use the day to select the correct SchoolPeriodType
            school_period_type = school_period_type_model.objects.filter(school=school, period_type=period_type).first()

            # If it's a Monday or a Wednesday, AND there are no school_period_types, filter it again using the normal schedule
            if school_period_type is None and (period_type == PERIOD_TYPE_MONDAY or period_type == PERIOD_TYPE_WEDNESDAY):
                school_period_type = school_period_type_model.objects.filter(school=school, period_type=PERIOD_TYPE_NORMAL).first()

            new_section_period_type = section_period_type_model(
                date=date,
                school=school,
                school_period_type=school_period_type
            )
            new_section_period_type.save()
            section_period_type = new_section_period_type

        else:
            school_period_type = section_period_type.school_period_type

        # Look for school periods with the selected school_period_type
        school_periods = school_period_model.objects.filter(school_period_type=school_period_type).order_by('period_number')
        section_period_type.edit_form = self.get_section_period_type_form(instance=section_period_type, school=school)

        return {
            'school_period_type': school_period_type, 
            'school_periods': school_periods,
            'section_period_type': section_period_type,
        }  

    def get_period_type_and_periods_view_schedule(self, school, date):
        section_period_model = apps.get_model(app_label='schedules', model_name='SectionPeriod')
        class_info = self.__get_class_info(school, date)

        # For each school period, check if there is any class/lesson plan for it
        for period in class_info['school_periods']:
            period.class_info = section_period_model.objects.get_class_period(period, date)

        return {
            'school_period_type': class_info['school_period_type'], 
            'school_periods': class_info['school_periods'],
            'section_period_type': class_info['section_period_type'],
        }    
    
    def get_section_period_type_form(self, instance, school):
        from schedules.forms import SectionPeriodTypeForm
        return SectionPeriodTypeForm(instance=instance, school=school)

    def get_school_period_type_form(self, instance):
        from schedules.forms import SchoolPeriodTypeForm
        return SchoolPeriodTypeForm(instance=instance)

    def get_period_type_and_periods(self, school, date):
        section_period_model = apps.get_model(app_label='schedules', model_name='SectionPeriod')
        class_info = self.__get_class_info(school, date)

        materials = []
        activities = []
        handouts = []
        flashcards = []

        # For each school period, check if there is any class/lesson plan for it
        for period in class_info['school_periods']:
            period.class_info = section_period_model.objects.get_class_period(period, date)
            if period.class_info is not None and period.class_info.lesson_plan is not None:
                activity_information = period.class_info.lesson_plan.get_all_info_from_all_activities()
                materials.extend(activity_information['materials'])
                for activity in activity_information['activities']:
                    if activity not in activities:
                        activities.append(activity)
                for handout in activity_information['handouts']:
                    if handout not in handouts:
                        handouts.append(handout)
                for flashcard in activity_information['flashcards']:
                    if flashcard not in flashcards:
                        flashcards.append(flashcard)
        
        materials = list(set(materials))

        return {
            'school_period_type': class_info['school_period_type'], 
            'school_periods': class_info['school_periods'],
            'section_period_type': class_info['section_period_type'],
            'materials': materials,
            'activities': activities,
            'handouts': handouts,
            'flashcards': flashcards,
        }

    def get_periods_and_profiles(self, school):
        school_period_model = apps.get_model(app_label='schedules', model_name='SchoolPeriod')
        period_type_query = super(SchoolPeriodTypeManager, self).get_queryset().filter(school=school)
        all_periods = []
        
        for period_type in period_type_query:
            period_type_object = {
                'type': period_type, 
                'period_type_text': period_type.get_period_type_text(),
                'period_type_color': period_type.get_period_type_color(),
                'periods': [], 
                'edit_period_form': self.get_school_period_type_form(instance=period_type)
            }
            period_query = school_period_model.objects.filter(school_period_type=period_type).order_by('period_number').values()
            periods = []
            for period in period_query:
                periods.append(period)
            period_type_object['periods'] = periods
            all_periods.append(period_type_object)

        return all_periods

    def append_period_to_array(self, period_array, period_number, start_time, end_time):
        period_array.append({
            'period_number': period_number,
            'start_time': start_time,
            'end_time': end_time,
        })
        return period_array

    def add_default_period(self, school):
        school_period_type_model = apps.get_model(app_label='schedules', model_name='SchoolPeriodType')
        school_period_model = apps.get_model(app_label='schedules', model_name='SchoolPeriod')
        
        old_period_types = school_period_type_model.objects.filter(school=school)
        old_periods = school_period_model.objects.filter(school_period_type=old_period_types)
        old_period_types.delete()

        all_period_types = []

        for item in ALL_SCHOOL_PERIODS[school.school_type]:
            school_periods = []
            for period in item['periods']:
                school_periods = SchoolPeriodTypeManager().append_period_to_array(
                    school_periods, period['number'], period['start'], period['end'])

            all_period_types.append({
                'period_type': school_period_type_model(
                    school=school,
                    period_name=item['period_name'],
                    period_type=item['period_type']
                ), 
                'period_array': school_periods
            })

        for item in all_period_types:
            item['period_type'].save()
            for period in item['period_array']:
                new_period = school_period_model(
                    school_period_type=item['period_type'],
                    period_number=period['period_number'],
                    start_time=period['start_time'],
                    end_time=period['end_time']
                )
                new_period.save()

class SchoolPeriodManager(models.Manager):
    def update_period_time(self, primary_key, value, is_start_time):
        school_period_model = apps.get_model(app_label='schedules', model_name='SchoolPeriod')
        school_period = school_period_model.objects.get(id=primary_key)
        if is_start_time:
            school_period.start_time=value
        else:
            school_period.end_time=value
        school_period.save()

class SchoolSectionManager(models.Manager):
    def add_default_school_sections(self, school):
        school_section_model = apps.get_model(app_label='schedules', model_name='SchoolSection')
        section_model = apps.get_model(app_label='schedules', model_name='Section')
        
        old_year_levels = school_section_model.objects.filter(school=school)
        old_sections = section_model.objects.filter(school_section=old_year_levels)
        old_year_levels.delete()
        old_sections.delete()

        if school.school_type == ELEMENTARY_SCHOOL:
            special_needs_section_name = '1'
            default_section_count = 4
            # Elementary school is from grades 1 to 6
            for year_level in range(1, 7): 
                new_year_level = school_section_model(
                    school=school,
                    year_level=year_level,
                    section_count=default_section_count
                )
                new_year_level.save()

                # Four sections per year level
                section_count_index = default_section_count + 1
                for section_number in range(1, section_count_index):
                    new_section = section_model(
                        school_section=new_year_level,
                        section_name=str(section_number),
                        teacher_name='',
                        notes=''
                    )
                    new_section.save()

        else:
            special_needs_section_name = 'A'
            default_section_count = 3
            # Junior high school is from grades 7 to 9
            for year_level in range(1, 4): 
                new_year_level = school_section_model(
                    school=school,
                    year_level=year_level,
                    section_count=default_section_count
                )
                new_year_level.save()

                # Three sections per year level
                section_count_index = default_section_count + 1
                for section_number in range(1, section_count_index):
                    character_section_number = chr(64+section_number)
                    new_section = section_model(
                        school_section=new_year_level,
                        section_name=str(character_section_number),
                        teacher_name='',
                        notes=''
                    )
                    new_section.save()

        # Add special needs
        special_year_level = school_section_model(
            school=school,
            year_level=0,
            section_count=1,
            is_special_needs=True
        )
        special_year_level.save()
        new_section = section_model(
            school_section=special_year_level,
            section_name=special_needs_section_name,
            teacher_name='',
            notes=''
        )
        new_section.save()

class SectionPeriodManager(models.Manager):
    def get_class_period(self, school_period, date):
        section_period_model = apps.get_model(app_label='schedules', model_name='SectionPeriod')
        return section_period_model.objects.filter(
            school_period=school_period,
            date=date).first()

    def get_year_level_dropdown(self, school):
        school_section_model = apps.get_model(app_label='schedules', model_name='SchoolSection')
        section_model = apps.get_model(app_label='schedules', model_name='Section')
        lesson_model = apps.get_model(app_label='lessons', model_name='Lesson')
        lesson_plan_model = apps.get_model(app_label='lessons', model_name='LessonPlan')
        school_section_course_model = apps.get_model(app_label='schedules', model_name='SchoolSectionCourse')

        all_year_levels = school_section_model.objects.filter(school=school).order_by('year_level')
        for year_level in all_year_levels:
            year_level.sections = json.dumps(list(section_model.objects.filter(school_section=year_level).values('id', 'section_name').order_by('section_name')))
            all_lesson_plans = []

            section_courses = school_section_course_model.objects.filter(school_section=year_level)
            for section_course in section_courses:
                related_lesson = lesson_model.objects.filter(course=section_course.course)
                all_lesson_plans.extend(list(lesson_plan_model.objects.filter(lesson__in=related_lesson, is_premade_lesson_plan=True).values('id', 'lesson__lesson_number', 'hour_number', 'lesson__course__course_name')))

            # If there are still no lesson plans by this point, check the generic lesson plans
            if len(all_lesson_plans) == 0:
                all_lesson_plans.extend(list(lesson_plan_model.objects.filter(topic__isnull=False).values('id', 'topic__name', 'hour_number')))

            year_level.lesson_plans = json.dumps(all_lesson_plans)

        return all_year_levels

    def get_last_lesson_hour(self, section, date):
        section_period_model = apps.get_model(app_label='schedules', model_name='SectionPeriod')
        period = section_period_model.objects.filter(section=section, date__lte=date).order_by('date')
        if period.exists():
            return period.latest('date')
        else:
            return None
