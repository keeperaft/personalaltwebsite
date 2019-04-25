import os
from django.dispatch import receiver

from lessons.constants import *
from lessons.filefield import ContentTypeRestrictedFileField
from lessons.managers import *
from paw.constants.models import *


class Course(models.Model):
    course_name = models.CharField(max_length=32)
    course_code = models.CharField(max_length=12)
    objects = CourseManager()

    def __str__(self):
        return self.course_name

class Lesson(models.Model):
    course = models.ForeignKey(Course)
    lesson_number = models.SmallIntegerField()
    title = models.CharField(max_length=128)
    objects = LessonManager()

    def __str__(self):
        return '%s, Lesson %s' % (self.course.course_code, self.lesson_number)

class Activity(models.Model):
    # For normal activities from the book
    activity_source_type = models.CharField(
        max_length=32,
        choices=ACTIVITY_SOURCE_TYPES,
        default=BOOK_FREE,
    )
    lesson = models.ForeignKey(Lesson, null=True)

    activity_skill_type = models.CharField(
        max_length=32,
        choices=ACTIVITY_SKILL_TYPES,
        default=VOCABULARY,
    )
    activity_name = models.CharField(max_length=256)
    description = models.TextField()
    materials = models.CharField(max_length=256, default=None)

    # For generic activities
    activity_portion_type = models.CharField(
        max_length=32,
        choices=ACTIVITY_PORTION_TYPES,
        default=None,
        null=True
    )
    objects = ActivityManager()

    def set_readable_skill_type(self):
        for item in ACTIVITY_SKILL_TYPES:
            if self.activity_skill_type == item[0]:
                self.activity_skill_type = item[1]

    def set_readable_portion_type(self):
        for item in ACTIVITY_PORTION_TYPES:
            if self.activity_portion_type == item[0]:
                self.activity_portion_type = item[1]

    def is_generic_activity(self):
        return self.lesson is None

    def get_generic_activity_form(self, instance):
        from lessons.forms import GenericActivityForm
        return GenericActivityForm(instance=instance)

    def get_activity_form(self, instance):
        from lessons.forms import ActivityForm
        return ActivityForm(instance=instance)

    def __init__(self, *args, **kwargs):  
        super(Activity, self).__init__(*args, **kwargs)  
        if self.is_generic_activity():
            self.edit_form = self.get_generic_activity_form(instance=self)
        else:
            self.edit_form = self.get_activity_form(instance=self)

    def __str__(self):
        if self.lesson:
            lesson = self.lesson
            course_code = lesson.course.course_code
            lesson_number = str(lesson.lesson_number)
            return course_code+', Lesson '+lesson_number+', '+self.activity_name
        else:
            return self.activity_name

class ActivityFile(models.Model):
    activity = models.ForeignKey(Activity)
    activity_file = ContentTypeRestrictedFileField(upload_to='static/files/', content_types=['text/plain', 'image/*', 'audio/*', 'video/*', 'application/*'], max_upload_size=5242880)
    original_filename = models.CharField(max_length=128)
    notes = models.TextField()
    is_link_to_existing_file = models.BooleanField(default=False)

    def get_file_name(self):
        return os.path.basename(self.activity_file.name)

    def __str__(self):
        return " | ".join([str(self.activity_file),
                           os.path.basename(self.activity_file.name)])

class Topic(models.Model):
    name = models.CharField(max_length=64)
    notes = models.TextField()

    def __str__(self):
        return str(self.name)

class LessonPlan(models.Model):
    lesson = models.ForeignKey(Lesson, null=True)
    hour_number = models.SmallIntegerField(null=True)
    greeting = models.ForeignKey(Activity, related_name='greeting', null=True)
    warmup = models.ForeignKey(Activity, related_name='warmup', null=True)
    presentation = models.ForeignKey(Activity, related_name='presentation', null=True)
    practice = models.ForeignKey(Activity, related_name='practice', null=True)
    production = models.ForeignKey(Activity, related_name='production', null=True)
    cooldown = models.ForeignKey(Activity, related_name='cooldown', null=True)
    assessment = models.ForeignKey(Activity, related_name='assessment', null=True)
    is_premade_lesson_plan = models.BooleanField(default=True)
    topic = models.ForeignKey(Topic, null=True)
    objects = LessonPlanManager()
    # created_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __get_info_from_activity(self, activity):
        if activity:
            handouts = []
            flashcards = []
            activity_files = ActivityFile.objects.filter(activity=activity, is_link_to_existing_file=False).order_by('original_filename')
            for file in activity_files:
                handout = {'id': file.id, 'filename': file.original_filename}
                if handout not in handouts:
                    handouts.append(handout)

            if activity.lesson is not None:
                lesson = Lesson.objects.get(pk=activity.lesson.id)
                lesson_flashcards = FlashcardLesson.objects.filter(lesson=lesson)
                for lesson_flashcard in lesson_flashcards:
                    flashcard = {'id': lesson_flashcard.flashcard.id, 'flashcard': lesson_flashcard.flashcard.label}
                    if flashcard not in flashcards:
                        flashcards.append(flashcard)

            return {
                'materials': activity.materials,
                'handouts': handouts,
                'flashcards': flashcards,
                'activity': {
                    'id': activity.id,
                    'activity_name': activity.activity_name
                }
            }
        return None

    def __construct_lesson_plan_info_array(self, portion, materials, activities, handouts, flashcards):
        info = self.__get_info_from_activity(portion)
        if info is not None:
            info_materials = info['materials']
            if info_materials != '' and info_materials not in materials and info != '':
                materials.append(info_materials)

            if info['activity'] not in activities:
                activities.append(info['activity'])

            for handout in info['handouts']:
                if handout not in handouts:
                    handouts.append(handout)

            for flashcard in info['flashcards']:
                if flashcard not in flashcards:
                    flashcards.append(flashcard)

    def get_all_info_from_all_activities(self):
        materials = []
        activities = []
        handouts = []
        flashcards = []

        self.__construct_lesson_plan_info_array(self.greeting, materials, activities, handouts, flashcards)
        self.__construct_lesson_plan_info_array(self.warmup, materials, activities, handouts, flashcards)
        self.__construct_lesson_plan_info_array(self.presentation, materials, activities, handouts, flashcards)
        self.__construct_lesson_plan_info_array(self.practice, materials, activities, handouts, flashcards)
        self.__construct_lesson_plan_info_array(self.production, materials, activities, handouts, flashcards)
        self.__construct_lesson_plan_info_array(self.cooldown, materials, activities, handouts, flashcards)
        self.__construct_lesson_plan_info_array(self.assessment, materials, activities, handouts, flashcards)

        return {'materials': materials, 'activities': activities, 'handouts': handouts, 'flashcards': flashcards}

    def __str__(self):
        if self.lesson is not None:
            return "Course: "+self.lesson.course.course_name+", Lesson "+str(self.lesson.lesson_number)+", Hour "+str(self.hour_number)
        else:
            return "Special lesson plan with primary key: "+str(self.id)

class TargetLanguage(models.Model):
    target_language = models.CharField(max_length=128)
    color = models.CharField(
        max_length=32,
        choices=TARGET_LANGUAGE_TYPES,
        default=TARGET_LANGUAGE_RED)
    notes = models.CharField(max_length=64, null=True)
    lesson = models.ForeignKey(Lesson)
    objects = TargetLanguageManager()

    def get_readable_color(self):
        for color in TARGET_LANGUAGE_TYPES:
            if color[0] == self.color:
                return color[1]

    def get_hex_color(self):
        if self.color == TARGET_LANGUAGE_RED:
            return HEX_COLOR_TARGET_LANGUAGE_RED
        elif self.color == TARGET_LANGUAGE_BLUE:
            return HEX_COLOR_TARGET_LANGUAGE_BLUE
        return HEX_COLOR_BLACK

    def get_target_language_form(self, instance):
        from lessons.forms import TargetLanguageForm
        return TargetLanguageForm(instance=instance)

    def __str__(self):
        return self.target_language+' | '+str(self.lesson)

    def __init__(self, *args, **kwargs):  
        super(TargetLanguage, self).__init__(*args, **kwargs)
        self.edit_target_language_form = self.get_target_language_form(instance=self)

class Flashcard(models.Model):
    orientation = models.CharField(
        max_length=32,
        choices=ORIENTATIONS,
        default=PORTRAIT,
    )
    flashcard_type = models.CharField(
        max_length=32,
        choices=FLASHCARD_TYPES,
        default=PICTURE_LABEL,
    )
    # picture = models.FileField(upload_to='')
    picture = ContentTypeRestrictedFileField(upload_to='media/flashcards/', content_types=['image/png', 'image/jpeg'], max_upload_size=5242880) 
    label = models.CharField(max_length=128)
    notes = models.CharField(max_length=64)
    is_bordered = models.BooleanField(default=True)
    objects = FlashcardManager()

    def __init__(self, *args, **kwargs):  
        super(Flashcard, self).__init__(*args, **kwargs)
        self.edit_flashcard_form = self.get_flashcard_form(instance=self)

    def get_flashcard_form(self, instance):
        from lessons.forms import FlashcardForm
        return FlashcardForm(instance=instance)

    def get_readable_orientation(self):
        for orientation in ORIENTATIONS:
            if orientation[0] == self.orientation:
                return orientation[1]

    def get_readable_layout(self):
        for flashcard_type in FLASHCARD_TYPES:
            if flashcard_type[0] == self.flashcard_type:
                return flashcard_type[1]

    def __str__(self):
        return self.label

class FlashcardLesson(models.Model):
    flashcard = models.ForeignKey(Flashcard)
    lesson = models.ForeignKey(Lesson)
    is_link_to_existing_flashcard = models.BooleanField(default=False)

    def __str__(self):
        return " | ".join([self.flashcard.label,
                           self.lesson.title])
        