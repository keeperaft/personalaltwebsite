from django import forms
from django.forms import ModelForm

from schedules.constants import NAME_PERIOD, PERIOD_TYPE_TEXT, NAME_TEACHER, NAME_NOTES, NAME_STUDENT_COUNT, NAME_LESSON_NUMBER, NAME_HOUR_NUMBER, NAME_PERIOD_PROFILE
from schedules.models import SchoolPeriodType, Section, SectionPeriod, SectionPeriodType


class SchoolPeriodTypeForm(ModelForm):
    class Meta:
        model = SchoolPeriodType
        fields = ['period_name', 'period_type']
        widgets = {
            'period_name': forms.TextInput(),
            'period_type': forms.Select()
        }
        labels = {
            'period_name': NAME_PERIOD,
            'period_type': PERIOD_TYPE_TEXT,
        }

class SectionForm(ModelForm):
    class Meta:
        model = Section
        fields = ['teacher_name', 'notes', 'student_count']
        widgets = {
            'student_count': forms.NumberInput(),
        }
        labels = {
            'teacher_name': NAME_TEACHER,
            'notes': NAME_NOTES,
            'student_count': NAME_STUDENT_COUNT,
        }


class LessonHourForm(ModelForm):
    class Meta:
        model = SectionPeriod
        fields = ['lesson_number', 'hour_number']
        widgets = {
            'lesson_number': forms.NumberInput(),
            'hour_number': forms.NumberInput(),
        }
        labels = {
            'lesson_number': NAME_LESSON_NUMBER,
            'hour_number': NAME_HOUR_NUMBER,
        }

class SectionPeriodTypeForm(ModelForm):
    class Meta:
        model = SectionPeriodType
        fields = ['school_period_type']
        widgets = {
            'school_period_type': forms.Select(attrs={'class':'remove-dash-select'})
        }
        labels = {
            'school_period_type': NAME_PERIOD_PROFILE,
        }

    def __init__(self, school=None, *args, **kwargs):
        super(SectionPeriodTypeForm, self).__init__(*args, **kwargs)
        if school is not None:
            self.fields['school_period_type'].queryset = SchoolPeriodType.objects.filter(school=school)

