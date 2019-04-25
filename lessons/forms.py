from django import forms
from django.forms import ModelForm

from lessons.constants import *
from lessons.models import Activity, ActivityFile, Course, Lesson, Topic, TargetLanguage, Flashcard, LessonPlan


class ActivityForm(ModelForm):
    materials = forms.CharField(required=False)
    class Meta:
        model = Activity
        fields = [
            'activity_name', 
            'description', 
            'materials']
        widgets = {
            'activity_name': forms.TextInput(),
            'description': forms.Textarea(),
            'materials': forms.TextInput(),
        }
        labels = {
            'activity_name': NAME_ACTIVITY,
            'description': NAME_DESCRIPTION,
            'materials': NAME_MATERIALS,
        }
    def __init__(self, *args, **kwargs):
        super(ActivityForm, self).__init__(*args, **kwargs)
        self.fields['materials'].label = NAME_MATERIALS

class FileForm(ModelForm):
    notes = forms.CharField(required=False)
    class Meta:
        model = ActivityFile
        fields = ['activity_file', 'notes']
        widgets = {
            'activity_file': forms.FileInput(),
            'notes': forms.TextInput(),
        }
        labels = {
            'activity_file': NAME_ACTIVITY_FILE,
            'notes': NAME_NOTES,
        }
    def __init__(self, *args, **kwargs):
        super(FileForm, self).__init__(*args, **kwargs)
        self.fields['notes'].label = NAME_NOTES

class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'course_code']
        widgets = {
            'course_name': forms.TextInput(),
            'course_code': forms.TextInput(),
        }
        labels = {
            'course_name': NAME_COURSE_NAME,
            'course_code': NAME_SHORT,
        }

class CourseDropdownForm(ModelForm):
    book = forms.ModelChoiceField(queryset=Course.objects.all().order_by('course_name'), empty_label='None')
    class Meta:
        model = Course
        fields = ['book']
        labels = {'book': NAME_BOOK}
    def __init__(self, *args, **kwargs):
        super(CourseDropdownForm, self).__init__(*args, **kwargs)
        self.fields['book'].label = NAME_BOOK

class LessonForm(ModelForm):
    class Meta:
        model = Lesson
        fields = ['title']
        widgets = {'title': forms.TextInput()}
        labels = {
            'title': NAME_TITLE,
        }

class GenericActivityForm(ModelForm):
    materials = forms.CharField(required=False)
    class Meta:
        model = Activity
        fields = [
            'activity_name', 
            'description', 
            'activity_portion_type',
            'materials']
        widgets = {
            'activity_name': forms.TextInput(),
            'description': forms.Textarea(),
            'activity_portion_type': forms.Select(),
            'materials': forms.TextInput(),
        }
        labels = {
            'activity_name': NAME_ACTIVITY_NAME,
            'description': NAME_DESCRIPTION,
            'activity_portion_type': NAME_ACTIVITY_PORTION_TYPE,
            'materials': NAME_MATERIALS,
        }
    def __init__(self, *args, **kwargs):
        super(GenericActivityForm, self).__init__(*args, **kwargs)
        self.fields['materials'].label = NAME_MATERIALS

class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = ['name', 'notes']
        widgets = {
            'name': forms.TextInput(),
            'notes': forms.TextInput(),
        }
        labels = {
            'name': NAME_NAME,
            'notes': NAME_NOTES,
        }

class LessonPlanForm(ModelForm):
    class Meta:
        model = LessonPlan
        fields = [
            'greeting',
            'warmup',
            'presentation',
            'practice',
            'production',
            'cooldown',
            'assessment'
        ]
        widgets = {
            'greeting': forms.Select(),
            'warmup': forms.Select(),
            'presentation': forms.Select(),
            'practice': forms.Select(),
            'production': forms.Select(),
            'cooldown': forms.Select(),
            'assessment': forms.Select(),
        }
        labels = {
            'greeting': NAME_GREETING,
            'warmup': NAME_WARMUP,
            'presentation': NAME_PRESENTATION,
            'practice': NAME_PRACTICE,
            'production': NAME_PRODUCTION,
            'cooldown': NAME_COOLDOWN,
            'assessment': NAME_ASSESSMENT,
        }

    def __init__(self, lessons, *args, **kwargs):
        super(LessonPlanForm, self).__init__(*args, **kwargs)
        self.fields['greeting'].queryset = self.get_activities_with_portion(GREETING, lessons)
        self.fields['warmup'].queryset = self.get_activities_with_portion(WARMUP, lessons)
        self.fields['presentation'].queryset = self.get_activities_with_portion(PRESENTATION, lessons)
        self.fields['practice'].queryset = self.get_activities_with_portion(PRACTICE, lessons)
        self.fields['production'].queryset = self.get_activities_with_portion(PRODUCTION, lessons)
        self.fields['cooldown'].queryset = self.get_activities_with_portion(COOLDOWN, lessons)
        self.fields['assessment'].queryset = self.get_activities_with_portion(ASSESSMENT, lessons)

    def get_activities_with_portion(self, activity_portion_type, lessons=None):
        return_instance = Activity.objects.filter(activity_portion_type=activity_portion_type, lesson=None)

        if activity_portion_type != GREETING and lessons is not None:
            for lesson in lessons:
                activity_instance = Activity.objects.filter(lesson=lesson)
                return_instance = return_instance.union(activity_instance)

        generic_activities = Activity.objects.filter(activity_portion_type=GENERIC, lesson=None)
        return_instance = return_instance.union(generic_activities)
        
        return return_instance

class TargetLanguageForm(ModelForm):
    notes = forms.CharField(required=False)
    class Meta:
        model = TargetLanguage
        fields = ['target_language', 'color', 'notes']
        widgets = {
            'target_language': forms.TextInput(),
            'color': forms.Select(),
            'notes': forms.TextInput(),
        }
        requireds = {
            'notes': False
        }
        labels = {
            'target_language': NAME_TARGET_LANGUAGE,
            'color': NAME_COLOR,
            'notes': NAME_NOTES,
        }
    def __init__(self, *args, **kwargs):
        super(TargetLanguageForm, self).__init__(*args, **kwargs)
        self.fields['notes'].label = NAME_NOTES


class FlashcardForm(ModelForm):
    class Meta:
        model = Flashcard
        fields = ['picture', 'label', 'orientation', 'flashcard_type', 'is_bordered', 'notes']
        widgets = {
            'picture': forms.FileInput(),
            'label': forms.TextInput(),
            'notes': forms.TextInput(),
            'orientation': forms.Select(),
            'flashcard_type': forms.Select(),
            'is_bordered': forms.CheckboxInput(attrs={'class':'toggle-switch', 'data-on-color': 'success', 'data-on-text':'Bordered', 'data-off-text':'No Border'}),
        }
        labels = {
            'picture': NAME_PICTURE,
            'label': NAME_LABEL,
            'notes': NAME_NOTES,
            'orientation': NAME_ORIENTATION,
            'flashcard_type': NAME_FLASHCARD_TYPE,
            'is_bordered': NAME_FLASHCARD_BORDER,
        }