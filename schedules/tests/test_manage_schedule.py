import time, os
import selenium
from schedules.models import *
from lessons.models import *
from paw.constants.tests import *
from paw.constants.models import *
from schedules.constants import *
from datetime import datetime, timedelta
from selenium.webdriver.common.keys import Keys
from schedules.tests.tests import ScheduleTestMethods
from schoolyears.models import SchoolYear, School, YearlySchedule
from lessons.constants import GREETING, WARMUP, PRESENTATION, PRACTICE, PRODUCTION, COOLDOWN, ASSESSMENT, GENERIC

class ScheduleManagementTestCases(ScheduleTestMethods):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    # Actions
    def __add_schedule_week(self):
        school = School.objects.get(name='Dolphin Elementary School')
        school_year = SchoolYear.objects.get(name='20XY ~ 20XZ')
        current_date = datetime.now()
        monday = None
        wednesday = None
        for i in range(0,7):
            scheduled_date = current_date + timedelta(days=i)
            weekday = scheduled_date.weekday()
            if weekday == 0: # Monday
                monday = scheduled_date
            elif weekday == 2: # Wednesday
                wednesday = scheduled_date
            if i > 0:
                super().add_yearly_schedule(school_year, school, scheduled_date)
        
        return {'monday': monday, 'wednesday': wednesday}

    def __click_view_schedule_button(self):
        super().click_button('view-schedule-button')
        time.sleep(PAGE_LOADING_LONG_WAIT_TIME)

    def __add_elementary_school_class(self, year_level, section, period_number):
        current_date = datetime.now()
        school = School.objects.get(name='Dolphin Elementary School')
        school_section = SchoolSection.objects.get(school=school, year_level=str(year_level))

        weekday = current_date.weekday() # 0 is Monday, 6 is Saturday
        period_type = PERIOD_TYPE_NORMAL
        if weekday == 0:
            period_type = PERIOD_TYPE_MONDAY
        elif weekday == 2:
            period_type = PERIOD_TYPE_WEDNESDAY
        school_period = SchoolPeriod.objects.get(period_number=period_number, school_period_type=SchoolPeriodType.objects.get(school=school, period_type=period_type))

        new_section_period = SectionPeriod(
            date=current_date,
            section=Section.objects.get(school_section=school_section, section_name=str(section)),
            school_period=school_period,
            lesson_plan=LessonPlan.objects.get(topic=None),
            lesson_number=1,
            hour_number=1,
        )
        new_section_period.save()

    def __fill_add_class_modal(self, year_level, section, lesson_plan):
        if year_level is not None:
            super().choose_option_from_select('id_year_level', year_level)
        if section is not None:
            super().choose_option_from_select('id_section', section)
        if lesson_plan is not None:
            super().choose_option_from_select('id_lesson_plan', lesson_plan)
        else:
            super().assert_dropdown_enabled('id_lesson_plan', False)
        super().click_modal_save_button()
        time.sleep(PAGE_LOADING_WAIT_TIME)

    def __click_add_class_button(self):
        button = self.browser.find_element_by_css_selector('.add-class-button')
        button.click()
        time.sleep(MODAL_TRANSITION_WAIT_TIME)

    def __add_first_period_class(self, year_level, section, lesson_plan):
        self.__click_add_class_button()
        self.__fill_add_class_modal(year_level, section, lesson_plan)

    def __change_period_profile(self, period_profile):
        super().click_button('edit-period-profile-entry-button')
        time.sleep(MODAL_TRANSITION_WAIT_TIME)
        super().choose_option_from_select('id_school_period_type', period_profile)
        super().click_modal_save_button()
        time.sleep(PAGE_LOADING_WAIT_TIME)

    def __get_activity(self, portion_type):
        return Activity.objects.get(activity_portion_type=portion_type)

    def __go_to_first_period_lesson_plan(self):
        button = self.browser.find_element_by_class_name('btn-tertiary')
        button.click()

    def __select_lesson_plan_activity_edit(self, id_selector, selection_text):
        if selection_text is not None:
            super().choose_option_from_select(id_selector, selection_text)

    def __edit_lesson_plan(self, greeting, warmup, presentation, practice, production, cooldown, assessment):
        button = self.browser.find_element_by_css_selector('#edit-lesson-plan-button')
        button.click()
        time.sleep(MODAL_TRANSITION_WAIT_TIME)

        self.__select_lesson_plan_activity_edit('id_greeting', greeting)
        self.__select_lesson_plan_activity_edit('id_warmup', warmup)
        self.__select_lesson_plan_activity_edit('id_presentation', presentation)
        self.__select_lesson_plan_activity_edit('id_practice', practice)
        self.__select_lesson_plan_activity_edit('id_production', production)
        self.__select_lesson_plan_activity_edit('id_cooldown', cooldown)
        self.__select_lesson_plan_activity_edit('id_assessment', assessment)

        super().click_modal_save_button()
        time.sleep(PAGE_LOADING_WAIT_TIME)

    def __delete_first_period_class(self):
        button = self.browser.find_element_by_class_name('delete-class-button')
        button.click()

    def __edit_lesson_hour(self, lesson, hour):
        button = self.browser.find_element_by_class_name('edit-lesson-hour-button')
        button.click()
        time.sleep(MODAL_TRANSITION_WAIT_TIME)
        super().type_text_in_input('#id_lesson_number', lesson)
        super().type_text_in_input('#id_hour_number', hour)
        super().click_modal_save_button()
        time.sleep(PAGE_LOADING_WAIT_TIME)

    # Assertions
    def __assert_no_days_scheduled(self):
        content = self.browser.find_element_by_id('paw-main-content').text
        self.assertIn('There are no classes scheduled for the school on this month. Would you like to schedule a new class day?', content)

    def __assert_class_existence(self, section, teacher, lesson):
        content = self.browser.find_element_by_id('paw-main-content').text
        self.assertIn(section, content)
        self.assertIn(teacher, content)
        self.assertIn(lesson, content)

    def __assert_class_inexistence(self, section, teacher, lesson, is_similar_lesson_found=False):
        content = self.browser.find_element_by_id('paw-main-content').text
        self.assertNotIn(section, content)
        self.assertNotIn(teacher, content)
        if not is_similar_lesson_found:
            self.assertNotIn(lesson, content)

    def __assert_class_lesson_plan_existence(self, year_level, section_name, greeting, warmup, presentation, practice, production, cooldown, assessment, hour_number):
        date = datetime.now()
        school_section = SchoolSection.objects.get(
            school=School.objects.get(name='Dolphin Elementary School'),
            year_level=year_level
        )
        section = Section.objects.get(
            school_section=school_section,
            section_name=section_name
        )
        lesson_plan = LessonPlan.objects.filter(
            greeting=greeting,
            warmup=warmup,
            presentation=presentation,
            practice=practice,
            production=production,
            cooldown=cooldown,
            assessment=assessment,
        ).last()
        self.assertTrue(SectionPeriod.objects.get(
            date=date,
            section=section,
            lesson_plan=lesson_plan,
        ))

    def __assert_first_period_profile_value(self, value):
        content = self.browser.find_element_by_class_name('default-profile-marker').text
        self.assertEqual(value, content)

    def __assert_option_is_in_dropdown(self, option, dropdown_selector_id):
        is_in_dropdown = False
        css_selector_option = '#%s > option' % (dropdown_selector_id)
        option_elements = self.browser.find_elements_by_css_selector(css_selector_option)
        for element in option_elements:
            if element.text == option:
                is_in_dropdown = True
                break
        self.assertTrue(is_in_dropdown)
        return is_in_dropdown

    def __assert_all_options_are_in_dropdown(self, options, dropdown_selector_id):
        is_all_in_dropdown = True
        for option in options:
            if not self.__assert_option_is_in_dropdown(option, dropdown_selector_id):
                is_all_in_dropdown = False
                break
        self.assertTrue(is_all_in_dropdown)

    def __assert_class_addition_lesson_plan_dropdown_values(self, year_level, section, expected_values):
        self.__click_add_class_button()
        time.sleep
        if year_level is not None:
            super().choose_option_from_select('id_year_level', year_level)
        if section is not None:
            super().choose_option_from_select('id_section', section)

        self.__assert_all_options_are_in_dropdown(expected_values, 'id_lesson_plan')
        super().click_modal_cancel_button()

    def __assert_period_days(self, datetime_object, expected_day):
        expected_string = "%s %s" % (datetime_object.strftime("%B %d"), expected_day)
        content = self.browser.find_element_by_id('paw-main-content')
        self.assertIn(expected_string, content.text)

    def __assert_lesson_hour_existence(self, lesson, hour):
        self.assertTrue(SectionPeriod.objects.filter(lesson_number=lesson, hour_number=hour).exists())

    def __assert_period_class_next_day(self, year_level, section_name):
        current_date = datetime.now()
        self.__click_add_class_button()
        if year_level is not None:
            super().choose_option_from_select('id_year_level', year_level)
        if section_name is not None:
            super().choose_option_from_select('id_section', section_name)
        modal = self.browser.find_element_by_css_selector('.modal.fade.in')
        self.assertIn('Lesson 1, Hour 1, on %s'%(current_date.strftime("%B %d, %Y")), modal.text)

    # Tests
    # python3 manage.py test schedules.tests.test_manage_schedule.ScheduleManagementTestCases.test_no_school_years_available
    def test_no_school_years_available(self):
        super().go_to_schedules_page()
        super().assert_no_school_years()

    def test_no_schools_available(self):
        super().go_to_schedules_page_with_school_year()
        super().assert_dropdown_enabled('select[name="school-year"]', True)
        super().assert_dropdown_enabled('select[name="school"]', False)
        super().assert_dropdown_enabled('select[name="month"]', True)

    def test_no_class_available(self):
        super().go_to_schedules_page_complete()
        self.__click_view_schedule_button()
        self.__assert_no_days_scheduled()

    def test_add_class_correctly(self):
        super().go_to_schedules_page_with_complete_package()
        self.__click_view_schedule_button()
        self.__add_first_period_class('3', '1', 'Let\'s Try 1, Lesson 1, Hour 1')
        self.__assert_class_existence('3-1', 'Mr. Nogami', 'Lesson 1, Hour 1 (Let\'s Try 1)')

    def test_add_class_no_lesson_plans(self):
        super().go_to_schedules_page_with_scheduled_day()
        self.__click_view_schedule_button()
        self.__add_first_period_class('3', '1', None)
        self.__assert_class_existence('3-1', 'N/A', None)

    def test_add_class_generic_lesson_plans(self):
        super().go_to_schedules_page_with_generic_lesson_plan()
        self.__click_view_schedule_button()
        self.__add_first_period_class('1', '1', 'Animals, Hour 1')
        self.__assert_class_existence('1-1', 'N/A', 'Lesson 1, Hour 1 (Animals)')

    def test_add_class_no_teacher_name(self):
        super().go_to_schedules_page_with_complete_package()
        self.__click_view_schedule_button()
        self.__add_first_period_class('3', '2', 'Let\'s Try 1, Lesson 1, Hour 1')
        self.__assert_class_existence('3-2', 'N/A', 'Lesson 1, Hour 1 (Let\'s Try 1)')

    def test_edit_period_profile(self):
        new_period_profile = 'Monday Schedule'
        super().go_to_schedules_page_with_complete_package()
        self.__click_view_schedule_button()
        self.__change_period_profile(new_period_profile)
        self.__assert_first_period_profile_value(new_period_profile)

    def test_edit_period_profile_with_class(self):
        weekday = datetime.now().weekday() # 0 is Monday, 6 is Saturday
        period_type = NAME_WEDNESDAY_SCHEDULE
        if weekday == 0 or weekday == 2:
            period_type = NAME_NORMAL_SCHEDULE

        super().go_to_schedules_page_with_class()
        self.__click_view_schedule_button()
        self.__change_period_profile(period_type)
        self.__assert_class_inexistence('3-1', 'Mr. Nogami', 'Lesson 1, Hour 1 (Let\'s Try 1)')

    def test_edit_return_period_profile_with_class(self):
        weekday = datetime.now().weekday() # 0 is Monday, 6 is Saturday
        
        old_period_type = NAME_NORMAL_SCHEDULE
        new_period_type = NAME_WEDNESDAY_SCHEDULE
        if weekday == 0:
            old_period_type = NAME_MONDAY_SCHEDULE
            new_period_type = NAME_NORMAL_SCHEDULE
        elif weekday == 2:
            old_period_type = NAME_WEDNESDAY_SCHEDULE
            new_period_type = NAME_NORMAL_SCHEDULE

        super().go_to_schedules_page_with_class()
        super().click_button('view-schedule-button')
        time.sleep(PAGE_LOADING_LONG_WAIT_TIME) # The Edit Period Profile button fails to click if it's not a long wait time
        self.__change_period_profile(new_period_type)
        self.__assert_class_inexistence('3-1', 'Mr. Nogami', 'Lesson 1, Hour 1 (Let\'s Try 1)')
        self.__change_period_profile(old_period_type)
        self.__assert_class_existence('3-1', 'Mr. Nogami', 'Lesson 1, Hour 1 (Let\'s Try 1)')

    # Have 5-1 and 4-1 on a specific day. Add 5-2: "Same as 5-1" should be there, but not "Same as "4-1"
    def test_same_lesson_plan_dropdown(self):
        expected_values_5_2 = ['None', 'Same as 5-1, Lesson 1, Hour 1 (Let\'s Try 1)']
        expected_values_4_2 = ['None', 'Same as 4-1, Lesson 1, Hour 1 (Let\'s Try 1)']
        super().go_to_schedules_page_with_complete_package()
        self.__add_elementary_school_class(year_level=5, section=1, period_number=1)
        self.__add_elementary_school_class(year_level=4, section=1, period_number=2)
        self.__click_view_schedule_button()
        self.__assert_class_addition_lesson_plan_dropdown_values(year_level='5', section='2', expected_values=expected_values_5_2)
        self.__assert_class_addition_lesson_plan_dropdown_values(year_level='4', section='2', expected_values=expected_values_4_2)

    def test_same_lesson_plan(self):
        super().go_to_schedules_page_with_complete_package()
        self.__add_elementary_school_class(year_level=5, section=1, period_number=2)
        self.__click_view_schedule_button()
        self.__add_first_period_class('5', '2', 'Same as 5-1, Lesson 1, Hour 1 (Let\'s Try 1)')
        self.__assert_class_lesson_plan_existence(
            year_level=5,
            section_name='2',
            greeting=self.__get_activity(GREETING),
            warmup=self.__get_activity(WARMUP),
            presentation=self.__get_activity(PRESENTATION),
            practice=self.__get_activity(PRACTICE),
            production=self.__get_activity(PRODUCTION),
            cooldown=self.__get_activity(COOLDOWN),
            assessment=self.__get_activity(ASSESSMENT),
            hour_number=1,
        )

    def test_same_lesson_plan_change_child_lsp(self):
        greeting = 'Hello Song'
        warmup = 'Rainbow Song'
        presentation_5_2 = 'None'
        presentation_5_1 = 'Vocabulary Drilling'
        practice = 'Keyword Game'
        production = 'Interview Game'
        cooldown = 'Signature Count'
        assessment = 'Vocabulary Volunteer'

        super().go_to_schedules_page_with_complete_package()
        self.__add_elementary_school_class(year_level=5, section=1, period_number=2)
        self.__click_view_schedule_button()
        self.__add_first_period_class('5', '2', 'Same as 5-1, Lesson 1, Hour 1 (Let\'s Try 1)')

        self.__go_to_first_period_lesson_plan()
        self.__edit_lesson_plan(
            greeting=None, 
            warmup=None, 
            presentation=presentation_5_2, 
            practice=None, 
            production=None, 
            cooldown=None, 
            assessment=None)

        self.__assert_class_lesson_plan_existence(
            year_level=5,
            section_name='2',
            greeting=self.__get_activity(GREETING),
            warmup=self.__get_activity(WARMUP),
            presentation=None,
            practice=self.__get_activity(PRACTICE),
            production=self.__get_activity(PRODUCTION),
            cooldown=self.__get_activity(COOLDOWN),
            assessment=self.__get_activity(ASSESSMENT),
            hour_number=1,
        )

        self.__assert_class_lesson_plan_existence(
            year_level=5,
            section_name='1',
            greeting=self.__get_activity(GREETING),
            warmup=self.__get_activity(WARMUP),
            presentation=self.__get_activity(PRESENTATION),
            practice=self.__get_activity(PRACTICE),
            production=self.__get_activity(PRODUCTION),
            cooldown=self.__get_activity(COOLDOWN),
            assessment=self.__get_activity(ASSESSMENT),
            hour_number=1,
        )

    def test_same_lesson_plan_change_parent_lsp(self):
        greeting = 'Hello Song'
        warmup = 'Rainbow Song'
        presentation_5_1 = 'None'
        presentation_5_2 = 'Vocabulary Drilling'
        practice = 'Keyword Game'
        production = 'Interview Game'
        cooldown = 'Signature Count'
        assessment = 'Vocabulary Volunteer'

        super().go_to_schedules_page_with_complete_package()
        self.__add_elementary_school_class(year_level=5, section=1, period_number=1)
        self.__click_view_schedule_button()
        self.__add_first_period_class('5', '2', 'Same as 5-1, Lesson 1, Hour 1 (Let\'s Try 1)')

        self.__go_to_first_period_lesson_plan()
        self.__edit_lesson_plan(
            greeting=None, 
            warmup=None, 
            presentation=presentation_5_1,
            practice=None, 
            production=None, 
            cooldown=None, 
            assessment=None)

        self.__assert_class_lesson_plan_existence(
            year_level=5,
            section_name='1',
            greeting=self.__get_activity(GREETING),
            warmup=self.__get_activity(WARMUP),
            presentation=None,
            practice=self.__get_activity(PRACTICE),
            production=self.__get_activity(PRODUCTION),
            cooldown=self.__get_activity(COOLDOWN),
            assessment=self.__get_activity(ASSESSMENT),
            hour_number=1,
        )

        self.__assert_class_lesson_plan_existence(
            year_level=5,
            section_name='2',
            greeting=self.__get_activity(GREETING),
            warmup=self.__get_activity(WARMUP),
            presentation=self.__get_activity(PRESENTATION),
            practice=self.__get_activity(PRACTICE),
            production=self.__get_activity(PRODUCTION),
            cooldown=self.__get_activity(COOLDOWN),
            assessment=self.__get_activity(ASSESSMENT),
            hour_number=1,
        )

    def test_delete_class(self):
        super().go_to_schedules_page_with_complete_package()
        self.__add_elementary_school_class(year_level=3, section=1, period_number=1)
        self.__click_view_schedule_button()
        self.__add_first_period_class('3', '2', 'Same as 3-1, Lesson 1, Hour 1 (Let\'s Try 1)')

        self.__assert_class_existence('3-1', 'Mr. Nogami', 'Lesson 1, Hour 1 (Let\'s Try 1)')
        self.__assert_class_existence('3-2', 'N/A', 'Lesson 1, Hour 1 (Let\'s Try 1)')
        self.__delete_first_period_class()
        self.__assert_class_inexistence('3-1', 'Mr. Nogami', 'Lesson 1, Hour 1 (Let\'s Try 1)', is_similar_lesson_found=True)
        self.__assert_class_existence('3-2', 'N/A', 'Lesson 1, Hour 1 (Let\'s Try 1)')

    def test_view_schedule(self):
        super().go_to_schedules_page_with_complete_package()
        assertion_days = self.__add_schedule_week()
        self.__click_view_schedule_button()
        self.__assert_period_days(assertion_days['monday'], "Monday Schedule")
        self.__assert_period_days(assertion_days['wednesday'], "Wednesday Schedule")

    def test_edit_lesson_plan_hour(self):
        super().go_to_schedules_page_with_complete_package()
        self.__add_elementary_school_class(year_level=5, section=1, period_number=1)
        self.__click_view_schedule_button()
        self.__go_to_first_period_lesson_plan()
        self.__edit_lesson_hour(lesson=2, hour=3)
        self.__assert_lesson_hour_existence(lesson=2, hour=3)

    def test_last_class_held(self):
        super().go_to_schedules_page_with_complete_package()
        self.__add_elementary_school_class(year_level=5, section=1, period_number=1)
        self.__add_schedule_week()
        self.__click_view_schedule_button()
        self.__assert_period_class_next_day('5', '1')

    def test_print_lesson_plan(self):
        super().go_to_schedules_page_with_complete_package()
        self.__add_elementary_school_class(year_level=5, section=1, period_number=1)
        self.__click_view_schedule_button()
        self.__go_to_first_period_lesson_plan()
        button = self.browser.find_element_by_class_name('print-lesson-plan')
        button.click()
        super().assert_download_did_not_fail()

    def test_automatic_hour_increment(self):
        super().go_to_schedules_page_with_complete_package()
        self.__click_view_schedule_button()
        self.__add_first_period_class('5', '1', 'None')
        self.__add_first_period_class('5', '1', 'None')
        self.__assert_class_existence('5-1', 'N/A', 'Lesson 1, Hour 1')
        self.__assert_class_existence('5-1', 'N/A', 'Lesson 1, Hour 2')
