import time, os
import selenium
from lessons.models import *
from paw.constants.tests import *
from paw.constants.models import *
from lessons.constants import *
from datetime import datetime, timedelta
from selenium.webdriver.common.keys import Keys
from lessons.tests.tests import LessonTestMethods

class LessonPlanManagementTestCases(LessonTestMethods):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    # Actions
    def __select_lesson_plan_activity(self, id_selector, selection_text):
        if selection_text is not None:
            super().choose_option_from_select(id_selector, selection_text)

    def __fill_lesson_plan_modal(self, greeting, warmup, presentation, practice, production, cooldown, assessment, generic_activity_exists=False):
        self.__select_lesson_plan_activity('id_greeting', greeting)
        self.__select_lesson_plan_activity('id_warmup', warmup)
        self.__select_lesson_plan_activity('id_presentation', presentation)
        self.__select_lesson_plan_activity('id_practice', practice)
        self.__select_lesson_plan_activity('id_production', production)
        self.__select_lesson_plan_activity('id_cooldown', cooldown)
        self.__select_lesson_plan_activity('id_assessment', assessment)
        super().click_modal_save_button()
        time.sleep(PAGE_LOADING_WAIT_TIME)

    def __click_check_lesson_plan_button(self):
        button = self.browser.find_element_by_id('check-lesson-plan-button')
        button.click()
        time.sleep(PAGE_LOADING_WAIT_TIME)

    def __add_lesson_plan(self, greeting, warmup, presentation, practice, production, cooldown, assessment, hour_number=None):
        super().click_button('add-lesson-plan')
        time.sleep(MODAL_TRANSITION_WAIT_TIME)
        if hour_number is not None:
            self.__assert_modal_hour_number_equality(hour_number)
        self.__fill_lesson_plan_modal(
            greeting=greeting,
            warmup=warmup,
            presentation=presentation,
            practice=practice,
            production=production,
            cooldown=cooldown,
            assessment=assessment
        )

    def __select_lesson_plan_activity_edit(self, id_selector, selection_text):
        if selection_text is not None:
            super().choose_option_from_select(id_selector, selection_text)

    def __edit_first_lesson_plan(self, greeting, warmup, presentation, practice, production, cooldown, assessment):
        button = self.browser.find_element_by_class_name('edit-lesson-plan')
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

    # Assertions
    def __assert_modal_hour_number_equality(self, expected_hour_number):
        actual_hour_number = self.browser.find_element_by_id('new-hour-number').text
        self.assertEqual(expected_hour_number, actual_hour_number)

    def __assert_option_is_in_dropdown(self, option, dropdown_selector_id):
        is_in_dropdown = False
        css_selector_option = '%s > option' % (dropdown_selector_id)
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

    # Tests
    # python3 manage.py test lessons.test_manage_lesson_plans.LessonPlanManagementTestCases.test_no_books
    def test_no_books(self):
        super().go_to_lesson_plans_page()
        content = self.browser.find_element_by_id('paw-main-content').text
        self.assertIn('There are no books available.', content)
        self.assertIn('Would you like to add a new book?', content)

    def test_book_no_lesson(self):
        super().go_to_lesson_plans_page_with_book()
        self.assertTrue(self.browser.find_element_by_css_selector('select[name="course_id"]').is_enabled())
        self.__assert_option_is_in_dropdown('Let\'s Try 1', 'select[name="course_id"]')
        self.assertFalse(self.browser.find_element_by_css_selector('select[name="lesson_id"]').is_enabled())

    def test_add_lesson_plan(self):
        greeting = 'Hello Song'
        warmup = 'Rainbow Song'
        base_presentation = 'Vocabulary Drilling'
        base_practice = 'Keyword Game'
        presentation = 'LeTr1, Lesson 1, Keyword Game'
        practice = 'LeTr1, Lesson 1, Activity, p.23'
        production = 'Interview Game'
        cooldown = 'Signature Count'
        assessment = 'Vocabulary Volunteer'
        generic = 'Missing Game'

        greeting_dropdown = [greeting, generic]
        warmup_dropdown = [warmup, generic, presentation, practice]
        presentation_dropdown = [base_presentation, generic, presentation, practice]
        practice_dropdown = [base_practice, generic, presentation, practice]
        production_dropdown = [production, generic, presentation, practice]
        cooldown_dropdown = [cooldown, generic, presentation, practice]
        assessment_dropdown = [assessment, generic, presentation, practice]

        super().go_to_lesson_plans_with_book_activities()
        self.__click_check_lesson_plan_button()

        super().click_button('add-lesson-plan')
        self.__assert_all_options_are_in_dropdown(greeting_dropdown, '.modal.fade.in #id_greeting')
        self.__assert_all_options_are_in_dropdown(warmup_dropdown, '.modal.fade.in #id_warmup')
        self.__assert_all_options_are_in_dropdown(presentation_dropdown, '.modal.fade.in #id_presentation')
        self.__assert_all_options_are_in_dropdown(practice_dropdown, '.modal.fade.in #id_practice')
        self.__assert_all_options_are_in_dropdown(production_dropdown, '.modal.fade.in #id_production')
        self.__assert_all_options_are_in_dropdown(cooldown_dropdown, '.modal.fade.in #id_cooldown')
        self.__assert_all_options_are_in_dropdown(assessment_dropdown, '.modal.fade.in #id_assessment')

        self.__fill_lesson_plan_modal(
            greeting=greeting,
            warmup=warmup,
            presentation=presentation,
            practice=practice,
            production=production,
            cooldown=cooldown,
            assessment=assessment
        )

        presentation_name = 'Keyword Game'
        practice_name = 'Activity, p.23'

        super().assert_lesson_plan_existence(
            greeting=greeting,
            warmup=warmup,
            presentation=presentation_name,
            practice=practice_name,
            production=production,
            cooldown=cooldown,
            assessment=assessment,
            hour_number=1,
        )

    def test_add_second_lesson_plan(self):
        practice = 'Missing Game'
        super().go_to_lesson_plans_with_lesson_plan()
        self.__click_check_lesson_plan_button()
        self.__add_lesson_plan(
            greeting=None,
            warmup=None,
            presentation=None,
            practice=practice,
            production=None,
            cooldown=None,
            assessment=None,
            hour_number='2',
        )
        super().assert_lesson_plan_existence(
            greeting=None,
            warmup=None,
            presentation=None,
            practice=practice,
            production=None,
            cooldown=None,
            assessment=None,
            hour_number=2,
        )

    def test_edit_lesson_plan(self):
        greeting = 'Hello Song'
        warmup = 'Rainbow Song'
        presentation = 'LeTr1, Lesson 1, Keyword Game'
        presentation_name = 'Keyword Game'
        practice = 'Keyword Game'
        production = 'Interview Game'
        cooldown = 'Signature Count'
        assessment = 'Vocabulary Volunteer'
        super().go_to_lesson_plans_with_lesson_plan()
        self.__click_check_lesson_plan_button()
        self.__edit_first_lesson_plan(
            greeting=None,
            warmup=None,
            presentation=presentation,
            practice=None,
            production=None,
            cooldown=None,
            assessment=None,
        )
        super().assert_lesson_plan_existence(
            greeting=greeting,
            warmup=warmup,
            presentation=presentation_name,
            practice=practice,
            production=production,
            cooldown=cooldown,
            assessment=assessment,
            hour_number=1,
        )

    def test_download_lesson_plan(self):
        super().go_to_lesson_plans_with_lesson_plan()
        self.__click_check_lesson_plan_button()
        button = self.browser.find_element_by_class_name('print-lesson-plan')
        button.click()
        super().assert_download_did_not_fail()
