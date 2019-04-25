from django import forms
from django.forms import ModelForm

from schoolyears.constants import *
from schoolyears.models import SchoolYear, School, Path, Node, SchoolRoute


class SchoolYearForm(ModelForm):
    class Meta:
        model = SchoolYear
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'class':'datepicker form-control'}),
            'end_date': forms.DateInput(attrs={'class':'datepicker form-control'}),
        }
        labels = { 
            'start_date': NAME_START_DATE,
            'end_date': NAME_END_DATE,
        }

class SchoolForm(ModelForm):
    class Meta:
        model = School
        fields = ['name', 'name_kanji', 'school_type']
        widgets = {
            'name': forms.TextInput(),
            'name_kanji': forms.TextInput(),
            'school_type': forms.Select()
        }
        labels = { 
            'name': NAME_SCHOOL_NAME,
            'name_kanji': NAME_KANJI_NAME,
            'school_type': NAME_SCHOOL_TYPE,
        }
        requireds = {
            'name_kanji': False,
        }

class PathForm(ModelForm):
    class Meta:
        model = Path
        fields = ['travel_vehicle_name', 'start_time', 'end_time', 'cost']
        widgets = {
            'travel_vehicle_name': forms.TextInput(),
            'start_time': forms.TimeInput(attrs={'class':'form-control'}),
            'end_time': forms.TimeInput(attrs={'class':'form-control'}),
            'cost': forms.NumberInput(),
        }
        labels = {
            'travel_vehicle_name': NAME_TRAVEL_VEHICLE,
            'start_time': NAME_START_TIME,
            'end_time': NAME_END_TIME,
            'cost': NAME_COST,
        }

class NodeForm(ModelForm):
    class Meta:
        model = Node
        fields = ['name']
        widgets = {
            'name': forms.TextInput()
        }
        labels = {
            'name': NAME_STATION,
        }

class AddRouteForm(ModelForm):
    class Meta:
        model = SchoolRoute
        fields = ['route_name', 'source_name', 'destination_name', 'travel_method',
            'total_cost', 'is_round_trip', 'is_alt_meeting']
        widgets = {
            'route_name': forms.TextInput(),
            'source_name': forms.TextInput(),
            'destination_name': forms.TextInput(),
            'total_cost': forms.NumberInput(),
            'is_round_trip': forms.CheckboxInput(attrs={'class':'toggle-switch', 
                'data-on-color': 'success', 'data-on-text':'Round Trip', 'data-off-text':'One Way'}),
            'is_alt_meeting': forms.CheckboxInput(attrs={'class':'toggle-switch', 
                'data-on-color': 'success', 'data-on-text':'Yes', 'data-off-text':'No'}),
            'travel_method': forms.Select(),
        }
        labels = {
            'route_name': NAME_ROUTE,
            'source_name': NAME_SOURCE,
            'destination_name': NAME_DESTINATION,
            'travel_method': NAME_TRAVEL_METHOD,
            'is_round_trip': NAME_IS_ROUND_TRIP,
            'is_alt_meeting': NAME_IS_ALT_MEETING,
            'total_cost': NAME_TOTAL_COST,
        }