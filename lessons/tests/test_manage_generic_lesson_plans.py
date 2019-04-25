import time, os
import selenium
from lessons.models import *
from paw.constants.tests import *
from paw.constants.models import *
from lessons.constants import *
from datetime import datetime, timedelta
from selenium.webdriver.common.keys import Keys
from lessons.tests.tests import LessonTestMethods


class GenericLessonPlanManagementTestCases(LessonTestMethods):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    # Actions
    def __fill_topic_modal(self, name, notes):
        super().type_text_in_input('.modal.fade.in #id_name', name)
        super().type_text_in_input('.modal.fade.in #id_notes', notes)
        super().click_modal_save_button()
        time.sleep(PAGE_LOADING_WAIT_TIME)

    def __select_lesson_plan_activity(self, id_selector, selection_text, generic_activity_exists):
        if selection_text is not None:
            super().choose_option_from_select(id_selector, selection_text)
        elif not generic_activity_exists:
            self.assertTrue(len(self.browser.find_elements_by_css_selector('#%s'%(id_selector)))==0)

    def __select_lesson_plan_activity_edit(self, id_selector, selection_text):
        if selection_text is not None:
            super().choose_option_from_select(id_selector, selection_text)

    def __fill_lesson_plan_modal(self, greeting, warmup, presentation, practice, production, cooldown, assessment, generic_activity_exists=False):
        self.__select_lesson_plan_activity('id_greeting', greeting, generic_activity_exists)
        self.__select_lesson_plan_activity('id_warmup', warmup, generic_activity_exists)
        self.__select_lesson_plan_activity('id_presentation', presentation, generic_activity_exists)
        self.__select_lesson_plan_activity('id_practice', practice, generic_activity_exists)
        self.__select_lesson_plan_activity('id_production', production, generic_activity_exists)
        self.__select_lesson_plan_activity('id_cooldown', cooldown, generic_activity_exists)
        self.__select_lesson_plan_activity('id_assessment', assessment, generic_activity_exists)
        super().click_modal_save_button()
        time.sleep(PAGE_LOADING_WAIT_TIME)

    def __select_topic(self, name):
        super().choose_option_from_select('topic-selection', name, is_modal=False)
        check_button = self.browser.find_element_by_id('check-lesson-plan-button')
        check_button.click()
        time.sleep(PAGE_LOADING_WAIT_TIME)

    def __add_topic(self, name, notes):
        element = self.browser.find_element_by_link_text('add a new topic?')
        element.click()
        time.sleep(MODAL_TRANSITION_WAIT_TIME)
        self.__fill_topic_modal(name, notes)

    def __edit_topic(self, name, notes):
        self.__select_topic(name)
        super().click_button('edit-topic')
        time.sleep(MODAL_TRANSITION_WAIT_TIME)
        self.__fill_topic_modal(name, notes)

    def __delete_topic(self, name):
        self.__select_topic(name)
        super().click_button('delete-topic')
        time.sleep(PAGE_LOADING_WAIT_TIME)

    def __add_lesson_plan(self, greeting, warmup, presentation, practice, production, cooldown, assessment, hour_number=None, generic_activity_exists=False):
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
            assessment=assessment,
            generic_activity_exists=generic_activity_exists,
        )

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
    def __assert_topic_existence(self, name, notes):
        self.assertTrue(Topic.objects.filter(name=name, notes=notes).exists())
        content = self.browser.find_element_by_id('paw-main-content').text
        self.assertIn(name, content)

    def __assert_topic_inexistence(self, name):
        self.assertFalse(Topic.objects.filter(name=name).exists())
        content = self.browser.find_element_by_id('paw-main-content').text
        self.assertNotIn(name, content)

    def __assert_modal_hour_number_equality(self, expected_hour_number):
        actual_hour_number = self.browser.find_element_by_id('new-hour-number').text
        self.assertEqual(expected_hour_number, actual_hour_number)

    def __assert_material_existence(self, name, materials):
        content = self.browser.find_element_by_id('paw-main-content').text
        self.assertIn(name, content)
        self.assertIn(materials, content)

    # Tests
    # python3 manage.py test lessons.test_manage_generic_lesson_plans.GenericLessonPlanManagementTestCases.test_add_topic
    def test_add_topic(self):
        name = 'Animals'
        notes = 'Generic lesson plans about animals'
        super().go_to_generic_lesson_plans_page()
        self.__add_topic(name, notes)
        self.__assert_topic_existence(name, notes)

    def test_edit_topic(self):
        name = 'Insects'
        notes = 'Generic lesson plans about insects'
        super().go_to_generic_lesson_plans_with_topic()
        self.__edit_topic(name, notes)
        self.__assert_topic_existence(name, notes)

    def test_delete_topic(self):
        name = 'Animals'
        super().go_to_generic_lesson_plans_with_topic()
        self.__delete_topic(name)
        self.__assert_topic_inexistence(name)

    def test_add_lesson_plan(self):
        greeting = 'Hello Song'
        warmup = 'Rainbow Song'
        presentation = 'Vocabulary Drilling'
        practice = 'Keyword Game'
        production = 'Interview Game'
        cooldown = 'Signature Count'
        assessment = 'Vocabulary Volunteer'
        super().go_to_generic_lesson_plans_with_all_generic_activities_available()
        self.__select_topic('Animals')
        self.__add_lesson_plan(
            greeting=greeting,
            warmup=warmup,
            presentation=presentation,
            practice=practice,
            production=production,
            cooldown=cooldown,
            assessment=assessment,
        )
        super().assert_lesson_plan_existence(
            greeting=greeting,
            warmup=warmup,
            presentation=presentation,
            practice=practice,
            production=production,
            cooldown=cooldown,
            assessment=assessment,
            hour_number=1,
        )

    def test_add_incomplete_lesson_plan(self):
        greeting = None
        warmup = 'Rainbow Song'
        presentation = 'Vocabulary Drilling'
        practice = 'Keyword Game'
        production = 'Interview Game'
        cooldown = 'Signature Count'
        assessment = 'Vocabulary Volunteer'
        super().go_to_generic_lesson_plans_with_some_generic_activites_available()
        self.__select_topic('Animals')
        self.__add_lesson_plan(
            greeting=greeting,
            warmup=warmup,
            presentation=presentation,
            practice=practice,
            production=production,
            cooldown=cooldown,
            assessment=assessment,
        )
        super().assert_lesson_plan_existence(
            greeting=greeting,
            warmup=warmup,
            presentation=presentation,
            practice=practice,
            production=production,
            cooldown=cooldown,
            assessment=assessment,
            hour_number=1,
        )

    def test_add_second_lesson_plan(self):
        practice = 'Missing Game'
        super().go_to_generic_lesson_plans_with_lesson_plan()
        self.__select_topic('Animals')
        self.__add_lesson_plan(
            greeting=None,
            warmup=None,
            presentation=None,
            practice=practice,
            production=None,
            cooldown=None,
            assessment=None,
            hour_number='2',
            generic_activity_exists=True,
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

    def test_materials(self):
        practice = 'Missing Game'
        materials = 'CD, Nametags, Ohajiki Marbles, Bar Magnets, Books, Notebooks, Rulers, Erasers, Pencil Sharpeners, Number Cards, Small Cards'
        super().go_to_generic_lesson_plans_with_all_generic_activities_available()
        self.__select_topic('Animals')
        self.__add_lesson_plan(
            greeting=None,
            warmup=None,
            presentation=None,
            practice=practice,
            production=None,
            cooldown=None,
            assessment=None,
            hour_number='1',
            generic_activity_exists=True,
        )
        super().assert_lesson_plan_existence(
            greeting=None,
            warmup=None,
            presentation=None,
            practice=practice,
            production=None,
            cooldown=None,
            assessment=None,
            hour_number=1,
        )
        self.__assert_material_existence(practice, materials)

    def test_edit_lesson_plan(self):
        greeting = 'Hello Song'
        warmup = 'Rainbow Song'
        presentation = 'Missing Game'
        practice = 'Keyword Game'
        production = 'Interview Game'
        cooldown = 'Signature Count'
        assessment = 'Vocabulary Volunteer'
        super().go_to_generic_lesson_plans_with_lesson_plan()
        self.__select_topic('Animals')
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
            presentation=presentation,
            practice=practice,
            production=production,
            cooldown=cooldown,
            assessment=assessment,
            hour_number=1,
        )

    def test_print_lesson_plan(self):
        super().go_to_generic_lesson_plans_with_lesson_plan()
        self.__select_topic('Animals')
        button = self.browser.find_element_by_class_name('print-lesson-plan')
        button.click()
        time.sleep(MODAL_TRANSITION_WAIT_TIME)
        super().assert_download_did_not_fail()
