import json
from collections import OrderedDict

from django.apps import apps
from django.db import models
from django.db.models import Q

from lessons.constants import NAME_ADD_COURSE, ADD_COURSE_MODAL_ID, ADD_COURSE, BOOK_FREE, BOOK_BOUND, \
    ACTIVITY_PORTION_TYPES
from paw.constants.base import NAME, URL, IS_SELECTED, MODAL_ID


class CourseManager(models.Manager):
    def get_courses_and_lessons(self):
        course_model = apps.get_model(app_label='lessons', model_name='Course')
        lesson_model = apps.get_model(app_label='lessons', model_name='Lesson')

        course_query = course_model.objects.all()
        all_courses = []

        for course in course_query:
            course_object = {'course': course, 'lessons': []}
            lesson_query = lesson_model.objects.filter(course=course).values('id', 'lesson_number', 'title').order_by('lesson_number')
            lessons = []
            for lesson in lesson_query:
                lessons.append(lesson)
            course_object['lessons'] = json.dumps(lessons)
            all_courses.append(course_object)

        return all_courses

    def get_sidebar_courses(self, selected_id):
        all_courses = super(CourseManager, self).get_queryset().order_by('course_name')
        sidebar = OrderedDict()

        for course in all_courses:
            sidebar[course.id] = {
                NAME: course.course_name,
                URL: 'lessons/courses/'+str(course.id),
                IS_SELECTED: course.id == int(selected_id),
                MODAL_ID: None,
            }

        return sidebar

class LessonManager(models.Manager):
    def get_activity_form(self, instance):
        from lessons.forms import ActivityForm
        return ActivityForm(instance=instance)

    def get_flashcard_form(self):
        from lessons.forms import FlashcardForm
        return FlashcardForm()

    def get_lesson_form(self, instance):
        from lessons.forms import LessonForm
        return LessonForm(instance=instance)

    def get_file_form(self):
        from lessons.forms import FileForm
        return FileForm()

    def modify_activities(self, activities):
        activity_file_model = apps.get_model(app_label='lessons', model_name='ActivityFile')
        
        for activity in activities:
            activity.set_readable_skill_type()
            activity.edit_form = self.get_activity_form(instance=activity)
            if activity.activity_source_type == BOOK_FREE:
                activity.file_form = self.get_file_form()
                activity.files = activity_file_model.objects.filter(activity=activity)

    def get_all_lessons(self, course):
        lesson_model = apps.get_model(app_label='lessons', model_name='Lesson')
        activity_model = apps.get_model(app_label='lessons', model_name='Activity')
        flashcard_lesson_model = apps.get_model(app_label='lessons', model_name='FlashcardLesson')

        all_lessons = lesson_model.objects.filter(course=course).order_by('lesson_number')
        for lesson in all_lessons:
            lesson.form = self.get_lesson_form(instance=lesson)
            lesson.book_activities = activity_model.objects.filter(activity_source_type=BOOK_BOUND, lesson=lesson).order_by('activity_name')
            lesson.free_activities = activity_model.objects.filter(activity_source_type=BOOK_FREE, lesson=lesson).order_by('activity_name')
            lesson.book_activity_form = self.get_activity_form()
            lesson.free_activity_form = self.get_activity_form() # I need them to be different instances
            lesson.add_flashcard_form = self.get_flashcard_form()

            lesson.flashcards = flashcard_lesson_model.objects.filter(lesson=lesson).order_by('flashcard__label') 
            LessonManager().__modify_activities(lesson.book_activities)
            LessonManager().__modify_activities(lesson.free_activities)
        return all_lessons

class ActivityManager(models.Manager):
    def get_all_generic_activities(self):
        all_activities = OrderedDict()
        activity_model = apps.get_model(app_label='lessons', model_name='Activity')

        for item in ACTIVITY_PORTION_TYPES:
            activity_instance = activity_model.objects.filter(lesson=None, activity_portion_type=item[0]).order_by('activity_name')
            if activity_instance.exists():
                for activity in activity_instance:
                    activity.set_readable_skill_type()
                all_activities[item[1]] = activity_instance

        return all_activities

class LessonPlanManager(models.Manager):
    def get_lesson_plan_form(self, instance, lessons):
        from lessons.forms import LessonPlanForm
        return LessonPlanForm(instance=instance, lessons=lessons)

    def get_all_hours_from_lesson(self, lesson):
        lesson_plan_model = apps.get_model(app_label='lessons', model_name='LessonPlan')

        all_hours = lesson_plan_model.objects.filter(lesson=lesson, is_premade_lesson_plan=True).order_by('hour_number')
        for hour in all_hours:
            hour.edit_hour_form = self.get_lesson_plan_form(instance=hour, lessons=[lesson])
        return all_hours

    def get_all_hours_from_topic(self, topic):
        lesson_plan_model = apps.get_model(app_label='lessons', model_name='LessonPlan')
        all_hours = lesson_plan_model.objects.filter(topic=topic).order_by('hour_number')
        for hour in all_hours:
            hour.edit_hour_form = self.get_lesson_plan_form(instance=hour, lessons=None)
        return all_hours

class TargetLanguageManager(models.Manager):
    def search_target_language(self, search_term):
        target_language_model = apps.get_model(app_label='lessons', model_name='TargetLanguage')
        return target_language_model.objects.filter(Q(target_language__icontains=search_term)|Q(notes__icontains=search_term)).order_by('target_language')[:50]

class FlashcardManager(models.Manager):
    def search_flashcard(self, search_term=''):
        flashcard_model = apps.get_model(app_label='lessons', model_name='Flashcard')
        flashcard_lesson_model = apps.get_model(app_label='lessons', model_name='FlashcardLesson')
        
        flashcards = flashcard_model.objects.filter(Q(label__icontains=search_term)|Q(notes__icontains=search_term))[:50]
        flashcard_lesson = flashcard_lesson_model.objects.filter(flashcard__in=flashcards).order_by('flashcard__label')[:50]
        return flashcard_lesson
