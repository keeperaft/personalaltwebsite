from collections import OrderedDict
from django.conf.urls import url
from django.shortcuts import render, redirect
from django.db import models
from schoolyears.models import SchoolYear
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

from home.constants import DASHBOARD, MSG_ERR_NO_SCHOOL_YEARS
from paw.constants.base import *

# Decorators
def school_year_required(f):
    def wrap(request, *args, **kwargs):
        if SchoolYear.objects.all().count() == 0:
            messages.error(request, MSG_ERR_NO_SCHOOL_YEARS)
            return redirect('/schoolyears')
        return f(request, *args, **kwargs)
    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap

def get_value_of_bootstrap_switch_in_post(request, search_key):
    if search_key in request.POST:
        return True
    return False

def get_value_of_optional_field_in_post_or_none(request, field):
    if field in request.POST:
        return request.POST[field]
    return None

def get_or_none(model_object, latest_column=None, **kwargs):
    try:
        if latest_column is not None:
            return model_object.objects.filter(**kwargs).latest(latest_column)

    except:
        return None

def render_page(request,
                page='',
                context=None,
                sidebar={},
                selected_menu=HOME):

    if context is None:
        context = {}

    # Menus
    home = {
        NAME: NAME_HOME,
        URL: INDEX,
        IS_SELECTED: False,
    }
    school_years = {
        NAME: NAME_SCHOOL_YEARS,
        URL: SCHOOL_YEARS,
        IS_SELECTED: False,
    }

    lessons = {
        NAME: NAME_LESSONS,
        URL: LESSONS,
        IS_SELECTED: False,
    }

    schedules = {
        NAME: NAME_SCHEDULES,
        URL: SCHEDULES,
        IS_SELECTED: False,
    }

    # Build the menus and the submenus
    context[MENU] = OrderedDict()
    context[MENU][HOME] = home
    context[MENU][SCHEDULES] = schedules
    context[MENU][LESSONS] = lessons
    context[MENU][SCHOOL_YEARS] = school_years

    context[MENU][selected_menu][IS_SELECTED] = True
    context[SIDEBAR] = sidebar

    return render(request, selected_menu+'/'+page+HTML_SUFFIX, context)

class Url():
    def __init__(self, urlpatterns, views):
        self.urlpatterns = urlpatterns
        self.views = views

    def add_url(self, expression='', name='', method_name=None):
        specific_method_name = name if method_name is None else method_name
        method = getattr(self.views, specific_method_name)
        self.urlpatterns.append(url(regex=expression, view=method, name=name))
        