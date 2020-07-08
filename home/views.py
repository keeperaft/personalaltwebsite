import calendar
from collections import OrderedDict
from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.translation import LANGUAGE_SESSION_KEY
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_POST

from home.constants import *
from home.models import *
from paw.constants.base import *
from schoolyears.models import *
from schedules.models import *
from lessons.models import *
from datetime import datetime, timedelta
from schoolyears.constants import BLUE, GREEN, ELEMENTARY_SCHOOL, JUNIOR_HIGH_SCHOOL

from home.pdf import print_day_pdf, print_week_pdf
from paw.constants.base import MODAL_ID
from paw.constants.base import NAME, URL, IS_SELECTED, HOME
from paw.methods import render_page, school_year_required


def home_render_page(request,
                     page='index',
                     context={},
                     selected_sidebar=DASHBOARD):
    dashboard = {
        NAME: NAME_DASHBOARD,
        URL: DASHBOARD,
        IS_SELECTED: False,
        MODAL_ID: None,
    }
    about = {
        NAME: NAME_ABOUT,
        URL: ABOUT,
        IS_SELECTED: False,
        MODAL_ID: None,
    }

    sidebar = OrderedDict()
    sidebar[DASHBOARD] = dashboard
    sidebar[ABOUT] = about
    sidebar[selected_sidebar][IS_SELECTED] = True

    return render_page(request,
                       page,
                       context,
                       sidebar=sidebar,
                       selected_menu=HOME)

def index(request):
    context = {}
    # Get today's info: school, period type, classes, materials
    today = YearlySchedule.objects.get_schedule_information_for_day(datetime.now())

    # Get the next work day's info: school, period type, classes, materials
    tomorrow = YearlySchedule.objects.get_schedule_information_for_day(datetime.now() + timedelta(days=1))
    
    # Get this week's info: schools (+ALT Meeting), period types, classes
    week = []
    for i in range(0, 7):
        week.append(YearlySchedule.objects.get_schedule_information_for_day(datetime.now() + timedelta(days=i)))
    
    context['today'] = today
    context['tomorrow'] = tomorrow
    context['week'] = week

    return home_render_page(request,
                       page='index',
                       context=context,
                       selected_sidebar=DASHBOARD)

def print_day(request):
    return print_day_pdf(request.POST['date'])
    
def print_week(request):
    return print_week_pdf(request.POST['date'])

def about(request):
    return home_render_page(request,
        page='about',
        context={},
        selected_sidebar=ABOUT)

def language(request, language_id):
    valid_languages = ['en', 'ja']
    if language_id in valid_languages:
        request.session[LANGUAGE_SESSION_KEY] = language_id
        return HttpResponse('success')
    return HttpResponse('failure')

def remove_demo_info(request):
    request.session['is_demo_info_removed'] = True
    return HttpResponse('success')

def __add_school(school_colors, school_type, school_year, name, name_kanji, address, contact_number, website, principal, vice_principal, english_head_teacher):
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

def __add_yearly_schedule(school_year, school, date):
    schedule = YearlySchedule(
        school_year=school_year,
        school=school,
        date=date,
    )
    schedule.save()

def __add_null_lesson_plan():
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

def __add_scheduled_class(school, date, year_level, period_number, section_name):
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
        lesson_plan=__add_null_lesson_plan(),
        lesson_number=1,
        hour_number=1,
    )
    new_section_period.save()

def reset_database(request):
    # Delete all relevant tables
    TemplatePeriodType.objects.all().delete()
    TemplateSectionPeriod.objects.all().delete()
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
    dolphin_es = __add_school(
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
    shark_jhs = __add_school(
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

    __add_yearly_schedule(new_school_year, dolphin_es, today)
    __add_yearly_schedule(new_school_year, shark_jhs, tomorrow)

    __add_scheduled_class(
        school=dolphin_es,
        date=today, 
        year_level=3, 
        period_number=1, 
        section_name='1')
    __add_scheduled_class(
        school=dolphin_es,
        date=today, 
        year_level=3, 
        period_number=2, 
        section_name='2')

    __add_scheduled_class(
        school=shark_jhs,
        date=tomorrow, 
        year_level=2, 
        period_number=1, 
        section_name='A')
    __add_scheduled_class(
        school=shark_jhs,
        date=tomorrow, 
        year_level=2, 
        period_number=2, 
        section_name='B')
    return redirect('/index')

def __render_error_page(request, page, status):
    # Menus
    context = {}
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
    
    context[MENU][HOME][IS_SELECTED] = True
    context[SIDEBAR] = {}

    return render(request, page, context, status)

def server_error(request):
    return __render_error_page(request, page='500.html', status=500)

def page_not_found(request):
    return __render_error_page(request, page='404.html', status=404)

