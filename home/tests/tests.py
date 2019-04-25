import os, time
import selenium
from selenium import webdriver
from django.contrib.auth.models import User
from lessons.models import *
from schedules.models import *
from schoolyears.models import SchoolYear, School, YearlySchedule, SpecialYearlySchedule, SchoolRoute
from paw.constants.tests import *
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from schoolyears.constants import ELEMENTARY_SCHOOL, JUNIOR_HIGH_SCHOOL, KEY_MTG, KEY_WORKDAY

from datetime import datetime, timedelta
from django.test import Client
from selenium.webdriver.common.keys import Keys

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class HomeTestMethods(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(BROWSER_IMPLICIT_WAIT_TIME)

        user = User.objects.create(username='tester')
        user.set_password('testpassword')
        user.save()

        self.client = Client()
        self.client.login(username='tester', password='testpassword')

        cookie = self.client.cookies['sessionid']

        self.browser.get(self.live_server_url)  
        self.browser.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
        self.browser.refresh()
        self.browser.get(self.live_server_url)

    def tearDown(self):
        self.browser.quit()

    # User actions
    def click_button(self, button_name):
        self.browser.execute_script("$('button[name="+button_name+"]').click()")

    def click_a_tag(self, tag_id):
        element = self.browser.find_element_by_id(tag_id)
        element.click()

    def click_modal_save_button(self):
        self.browser.execute_script("$('.modal.fade.in .modal-footer .btn-primary').click();")
        time.sleep(PAGE_LOADING_WAIT_TIME)

    def click_toggle_switch(self, selector_id, should_click):
        if should_click:
            self.browser.execute_script("$('.modal.fade.in .bootstrap-switch input#%s').click();"%(selector_id))
            time.sleep(BOOTSTRAP_SWITCH_TRANSITION_WAIT_TIME)

    def type_text_in_input(self, css_selector, input_text):
        element = self.browser.find_element_by_css_selector(css_selector)
        element.clear()
        element.click()
        element.send_keys(input_text)
        
    def choose_option_from_select(self, selector_id, option_text, is_modal=True):
        css_selector = '.modal.fade.in #%s' % (selector_id)
        css_selector_option = '.modal.fade.in #%s > option' % (selector_id)
        if not is_modal:
            css_selector = '#%s' % (selector_id)
            css_selector_option = '#%s > option' % (selector_id)

        dropdown_element = self.browser.find_element_by_css_selector(css_selector)
        dropdown_element.click()

        option_elements = self.browser.find_elements_by_css_selector(css_selector_option)
        for element in option_elements:
            if element.text == option_text:
                element.click()
                break

    # Assertions used in multiple places
    def assert_download_did_not_fail(self):
        content = self.browser.find_element_by_css_selector('body').text
        self.assertNotIn('Exception Type', content)

    def assert_enabled(self, css_selector, is_enabled):
        self.assertTrue(self.browser.find_element_by_css_selector(css_selector).is_enabled() == is_enabled)

    def assert_no_school_years(self):
        error_message = 'This action is not possible if there are no school years available. Please add a school year first by clicking "+ Add New School Year".'
        content = self.browser.find_element_by_css_selector('body').text
        self.assertIn(error_message, content)

    # Go to certain pages
    def __add_new_course(self, name=None, code=None):
        if name is not None and code is not None:
            new_course = Course(
                course_name=name,
                course_code=code
            )
        else:
            new_course = Course(
                course_name='Let\'s Try 1',
                course_code='LeTr1'
            )
        new_course.save()
        return new_course

    def __add_new_lesson(self, course, lesson_number=None, title=None):
        if lesson_number is not None and title is not None:
            new_lesson = Lesson(
                course = course,
                lesson_number = lesson_number,
                title = title)
            new_lesson.save()
        else:
            new_lesson = Lesson(
                course = course,
                lesson_number = 1,
                title = 'Hello, world!')
            new_lesson.save()
        return new_lesson

    def __add_school_year(self):
        current_date = datetime.now()
        start_date = current_date - timedelta(days=100)
        end_date = current_date + timedelta(days=100)
        new_school_year = SchoolYear(
            name = '20XY ~ 20XZ',
            start_date = start_date,
            end_date = end_date,
            is_active = True
        )
        new_school_year.save()
        return new_school_year

    def __add_school(self):
        school_year = self.__add_school_year()
        elementary = School(
            school_type=ELEMENTARY_SCHOOL,
            school_year=school_year,
            name='Dolphin Elementary School',
            name_kanji='イルカ小学校'
        )
        elementary.save()
        junior_high = School(
            school_type=JUNIOR_HIGH_SCHOOL,
            school_year=school_year,
            name='Shark Junior High School',
            name_kanji='サメ中学校'
        )
        junior_high.save()
        return {'school_year': school_year, 'elementary': elementary, 'junior_high': junior_high}

    def add_yearly_schedule(self, school_year, school, date):
        schedule = YearlySchedule(
            school_year=school_year,
            school=school,
            date=date,
        )
        schedule.save()

    def __add_generic_activity_with_name_and_portion_type(self, name, portion_type, materials='CD, Ohajiki Marbles, Cats'):
        new_generic_activity = Activity(
            lesson=None,
            activity_skill_type=VOCABULARY,
            activity_name=name,
            description='A generic description about the activity',
            materials=materials,
            activity_portion_type=portion_type,
        )
        new_generic_activity.save()

    def __add_generic_activity_for_all_parts(self):
        self.__add_generic_activity_with_name_and_portion_type('Hello Song', GREETING)
        self.__add_generic_activity_with_name_and_portion_type('Missing Game', GENERIC, materials='CD, Nametags, Ohajiki Marbles, Bar Magnets, Books, Notebooks, Rulers, Erasers, Pencil Sharpeners, Number Cards, Small Cards')
        self.__add_generic_activity_with_name_and_portion_type('Rainbow Song', WARMUP)
        self.__add_generic_activity_with_name_and_portion_type('Vocabulary Drilling', PRESENTATION)
        self.__add_generic_activity_with_name_and_portion_type('Keyword Game', PRACTICE)
        self.__add_generic_activity_with_name_and_portion_type('Interview Game', PRODUCTION)
        self.__add_generic_activity_with_name_and_portion_type('Signature Count', COOLDOWN)
        self.__add_generic_activity_with_name_and_portion_type('Vocabulary Volunteer', ASSESSMENT)

    def __get_activity(self, portion_type):
        return Activity.objects.get(activity_portion_type=portion_type)

    def __add_non_generic_lesson_plan(self, lesson):
        self.__add_generic_activity_for_all_parts()
        new_lesson_plan = LessonPlan(
            hour_number=1,
            greeting=self.__get_activity(GREETING),
            warmup=self.__get_activity(WARMUP),
            presentation=self.__get_activity(PRESENTATION),
            practice=self.__get_activity(PRACTICE),
            production=self.__get_activity(PRODUCTION),
            cooldown=self.__get_activity(COOLDOWN),
            assessment=self.__get_activity(ASSESSMENT),
            lesson=lesson
        )
        new_lesson_plan.save()

    def __add_classes_today_tomorrow(self):
        schools = self.__add_school()
        current_date = datetime.now()
        course = self.__add_new_course()
        lesson = self.__add_new_lesson(course)
        self.__add_non_generic_lesson_plan(lesson)
        tomorrow = current_date + timedelta(days=1)
        self.add_yearly_schedule(schools['school_year'], schools['elementary'], current_date)
        self.add_yearly_schedule(schools['school_year'], schools['junior_high'], tomorrow)

    def __add_scheduled_class(self, date, year_level, section_name, period, is_elementary_school=False):
        if is_elementary_school:
            school = School.objects.get(name='Dolphin Elementary School')
        else:
            school = School.objects.get(name='Shark Junior High School')
        year_level = SchoolSection.objects.get(school=school, year_level=year_level)

        weekday = date.weekday() # 0 is Monday, 6 is Saturday
        period_type = PERIOD_TYPE_NORMAL
        if weekday == 0:
            period_type = PERIOD_TYPE_MONDAY
        elif weekday == 2:
            period_type = PERIOD_TYPE_WEDNESDAY
        
        school_period = SchoolPeriod.objects.get(period_number=period, school_period_type=SchoolPeriodType.objects.get(school=school, period_type=period_type))

        new_section_period = SectionPeriod(
            date=date,
            section=Section.objects.get(school_section=year_level, section_name=section_name),
            school_period=school_period,
            lesson_plan=LessonPlan.objects.get(hour_number=1),
            lesson_number=1,
            hour_number=1,
        )
        new_section_period.save()

    def __add_schedule_week(self):
        school = School.objects.get(name='Dolphin Elementary School')
        school_year = SchoolYear.objects.get(name='20XY ~ 20XZ')
        current_date = datetime.now()
        for i in range(0,7):
            scheduled_date = current_date + timedelta(days=i)
            self.add_yearly_schedule(school_year, school, scheduled_date)
            self.__add_scheduled_class(
                date=scheduled_date, 
                year_level='4', 
                section_name='1',
                period=1,
                is_elementary_school=True
            )
            self.__add_scheduled_class(
                date=scheduled_date, 
                year_level='4', 
                section_name='2',
                period=2,
                is_elementary_school=True
            )
            self.__add_scheduled_class(
                date=scheduled_date, 
                year_level='4', 
                section_name='3',
                period=3,
                is_elementary_school=True
            )

    def __add_alt_meeting_work_day(self):
        self.__add_school_year()
        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        school_year = SchoolYear.objects.get(name='20XY ~ 20XZ')
        
        alt_meeting = SpecialYearlySchedule(
            special_event=KEY_MTG,
            school_year=school_year,
            date=today,
        )
        alt_meeting.save()

        work_day = SpecialYearlySchedule(
            special_event=KEY_WORKDAY,
            school_year=school_year,
            date=tomorrow,
        )
        work_day.save()

    def go_to_dashboard(self):
        self.browser.get('%s%s' % (self.live_server_url, '/'))

    def go_to_dashboard_with_classes_for_today_and_tomorrow(self):
        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        self.__add_classes_today_tomorrow()
        self.__add_scheduled_class(
            date=today, 
            year_level='3', 
            section_name='1',
            period=1, 
            is_elementary_school=True
        )
        self.__add_scheduled_class(
            date=today, 
            year_level='3', 
            section_name='2',
            period=2, 
            is_elementary_school=True
        )
        self.__add_scheduled_class(
            date=tomorrow, 
            year_level='2', 
            section_name='A',
            period=1, 
            is_elementary_school=False
        )

        self.__add_scheduled_class(
            date=tomorrow, 
            year_level='2', 
            section_name='B',
            period=3, 
            is_elementary_school=False
        )
        self.browser.get('%s%s' % (self.live_server_url, '/'))

    def go_to_dashboard_with_classes_for_the_week(self):
        schools = self.__add_school()
        course = self.__add_new_course()
        lesson = self.__add_new_lesson(course)
        self.__add_non_generic_lesson_plan(lesson)
        self.__add_schedule_week()
        self.browser.get('%s%s' % (self.live_server_url, '/'))
        
    def go_to_dashboard_with_alt_meeting_work_day(self):
        self.__add_alt_meeting_work_day()
        self.browser.get('%s%s' % (self.live_server_url, '/'))

    ######################

    def go_to_timesheets_page(self):
        self.browser.get('%s%s' % (self.live_server_url, '/timesheets'))

    def go_to_timesheets_page_with_school_year(self):
        self.__add_school_year()
        self.browser.get('%s%s' % (self.live_server_url, '/timesheets'))

    def go_to_timesheets_page_with_school(self):
        self.__add_school()
        self.browser.get('%s%s' % (self.live_server_url, '/timesheets'))

    ######################

    def __add_school_with_route(self, is_schedule_included=True):
        schools = self.__add_school()
        new_route = SchoolRoute(
            school_year=schools['school_year'],
            school=schools['elementary'],
            route_name='Dolphin Elementary School',
            source_name='Dolphino Station',
            destination_name='Dolphin Elementary School Bus Stop',
            is_round_trip=True,
            total_cost=500,
            is_alt_meeting=False,
            calculated_total_cost=500,
        )
        new_route.save()
        if is_schedule_included:
            self.add_yearly_schedule(schools['school_year'], schools['elementary'], datetime.now())

    def go_to_reimbursements_page(self):
        self.browser.get('%s%s' % (self.live_server_url, '/reimbursements'))

    def go_to_reimbursements_page_with_complete_package(self):
        self.__add_school_with_route()
        self.browser.get('%s%s' % (self.live_server_url, '/reimbursements'))

    def go_to_reimbursements_page_with_school(self):
        self.__add_school_with_route(is_schedule_included=False)
        self.browser.get('%s%s' % (self.live_server_url, '/reimbursements'))

    def go_to_reimbursements_page_with_alt_meeting(self):
        schools = self.__add_school()
        new_route = SchoolRoute(
            school_year=schools['school_year'],
            school=None,
            route_name='Route to and from ALT Meeting',
            source_name='Dolphino Station',
            destination_name='Starfish Station',
            is_round_trip=True,
            total_cost=870,
            is_alt_meeting=True,
            calculated_total_cost=870,
        )
        new_route.save()
        today = datetime.now()        
        alt_meeting = SpecialYearlySchedule(
            special_event=KEY_MTG,
            school_year=schools['school_year'],
            date=today,
        )
        alt_meeting.save()
        self.browser.get('%s%s' % (self.live_server_url, '/reimbursements'))

    def go_to_settings_page(self):
        self.browser.get('%s%s' % (self.live_server_url, '/settings'))

    def go_to_404_page(self):
        self.browser.get('%s%s' % (self.live_server_url, '/40404'))

    def go_to_500_page(self):
        self.browser.get('%s%s' % (self.live_server_url, '/test_server_error'))
