import os, time
import selenium
from selenium import webdriver
from django.contrib.auth.models import User
from schedules.models import *
from schoolyears.models import SchoolYear, School, YearlySchedule
from paw.constants.tests import *
from lessons.models import *
from django.conf import settings
from schoolyears.constants import ELEMENTARY_SCHOOL, JUNIOR_HIGH_SCHOOL
from django.contrib.staticfiles.templatetags.staticfiles import static

from datetime import datetime, timedelta
from django.test import Client
from selenium.webdriver.common.keys import Keys

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class ScheduleTestMethods(StaticLiveServerTestCase):

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

    def click_modal_cancel_button(self):
        self.browser.execute_script("$('.modal.fade.in .modal-footer .btn-default').click();")
        time.sleep(MODAL_TRANSITION_WAIT_TIME)

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

    def assert_no_school_years(self):
        error_message = 'This action is not possible if there are no school years available. Please add a school year first by clicking "+ Add New School Year".'
        content = self.browser.find_element_by_css_selector('body').text
        self.assertIn(error_message, content)

    def assert_dropdown_enabled(self, css_selector, is_enabled):
        self.assertTrue(self.browser.find_element_by_css_selector(css_selector).is_enabled() == is_enabled)

    def assert_download_did_not_fail(self):
        content = self.browser.find_element_by_css_selector('body').text
        self.assertNotIn('Exception Type', content)

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

    def __add_generic_lesson_plan(self):
        self.__add_generic_activity_for_all_parts()
        new_topic = Topic(
            name='Animals',
            notes='Generic topic about animals'
        )
        new_topic.save()
        new_lesson_plan = LessonPlan(
            hour_number=1,
            greeting=self.__get_activity(GREETING),
            warmup=self.__get_activity(WARMUP),
            presentation=self.__get_activity(PRESENTATION),
            practice=self.__get_activity(PRACTICE),
            production=self.__get_activity(PRODUCTION),
            cooldown=self.__get_activity(COOLDOWN),
            assessment=self.__get_activity(ASSESSMENT),
            topic=new_topic,
        )
        new_lesson_plan.save()

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

    def __add_schedule_today(self):
        schools = self.__add_school()
        current_date = datetime.now()
        self.add_yearly_schedule(schools['school_year'], schools['elementary'], current_date)
        self.add_yearly_schedule(schools['school_year'], schools['junior_high'], current_date)

    def __add_book_to_third_grade(self):
        school = School.objects.get(name='Dolphin Elementary School')
        book = Course.objects.get(course_name='Let\'s Try 1')
        year_level = SchoolSection.objects.get(school=school, year_level='3')

        # Add teacher
        section = Section.objects.get(school_section=year_level, section_name='1')
        section.teacher_name = 'Mr. Nogami'
        section.save()

        year_level_book = SchoolSectionCourse(
            school_section=year_level,
            course=book
        )
        year_level_book.save()

    def __add_complete_package(self):
        self.__add_schedule_today()
        course = self.__add_new_course()
        lesson = self.__add_new_lesson(course)
        self.__add_non_generic_lesson_plan(lesson)
        self.__add_book_to_third_grade()

    def __add_scheduled_class(self):
        self.__add_complete_package()
        current_date = datetime.now()
        school = School.objects.get(name='Dolphin Elementary School')
        year_level = SchoolSection.objects.get(school=school, year_level='3')

        weekday = current_date.weekday() # 0 is Monday, 6 is Saturday
        period_type = PERIOD_TYPE_NORMAL
        if weekday == 0:
            period_type = PERIOD_TYPE_MONDAY
        elif weekday == 2:
            period_type = PERIOD_TYPE_WEDNESDAY
        school_period = SchoolPeriod.objects.get(period_number=1, school_period_type=SchoolPeriodType.objects.get(school=school, period_type=period_type))

        new_section_period = SectionPeriod(
            date=current_date,
            section=Section.objects.get(school_section=year_level, section_name='1'),
            school_period=school_period,
            lesson_plan=LessonPlan.objects.get(hour_number=1),
            lesson_number=1,
            hour_number=1,
        )
        new_section_period.save()

    def __add_generic_lesson_plan_package(self):
        self.__add_schedule_today()
        course = self.__add_new_course()
        lesson = self.__add_new_lesson(course)
        self.__add_generic_lesson_plan()

    def go_to_schedules_page(self):
        self.browser.get('%s%s' % (self.live_server_url, '/schedules/'))

    def go_to_schedules_page_with_school_year(self):
        self.__add_school_year()
        self.browser.get('%s%s' % (self.live_server_url, '/schedules/'))

    def go_to_schedules_page_complete(self):
        self.__add_school()
        self.browser.get('%s%s' % (self.live_server_url, '/schedules/'))

    def go_to_schedules_page_with_scheduled_day(self):
        self.__add_schedule_today()
        self.browser.get('%s%s' % (self.live_server_url, '/schedules/'))

    def go_to_schedules_page_with_complete_package(self):
        self.__add_complete_package()
        self.browser.get('%s%s' % (self.live_server_url, '/schedules/'))

    def go_to_schedules_page_with_class(self):
        self.__add_scheduled_class()
        self.browser.get('%s%s' % (self.live_server_url, '/schedules/'))

    def go_to_schedules_page_with_generic_lesson_plan(self):
        self.__add_generic_lesson_plan_package()
        self.browser.get('%s%s' % (self.live_server_url, '/schedules/'))

    ############

    def go_to_year_level_page(self):
        self.browser.get('%s%s' % (self.live_server_url, '/schedules/sections_courses'))

    def go_to_year_level_page_with_school_year(self):
        self.__add_school_year()
        self.browser.get('%s%s' % (self.live_server_url, '/schedules/sections_courses'))

    def go_to_year_level_with_school(self):
        self.__add_school()
        self.browser.get('%s%s' % (self.live_server_url, '/schedules/sections_courses'))

    def go_to_year_level_with_complete_package(self):
        self.__add_complete_package()
        self.browser.get('%s%s' % (self.live_server_url, '/schedules/sections_courses'))

    def go_to_year_level_with_scheduled_class(self):
        self.__add_scheduled_class()
        self.browser.get('%s%s' % (self.live_server_url, '/schedules/sections_courses'))

    ############

    def go_to_school_periods_page(self):
        self.browser.get('%s%s' % (self.live_server_url, '/schedules/school_periods'))

    def go_to_school_periods_page_with_school_year(self):
        self.__add_school_year()
        self.browser.get('%s%s' % (self.live_server_url, '/schedules/school_periods'))

    def go_to_school_periods_with_school(self):
        self.__add_school()
        self.browser.get('%s%s' % (self.live_server_url, '/schedules/school_periods'))
