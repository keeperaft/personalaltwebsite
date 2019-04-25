import time, os
import selenium
from lessons.models import *
from paw.constants.tests import *
from paw.constants.models import *
from lessons.constants import *
from datetime import datetime, timedelta
from selenium.webdriver.common.keys import Keys
from lessons.tests.tests import LessonTestMethods

class GenericActivityManagementTestCases(LessonTestMethods):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    # Actions
    def __fill_generic_activity_fields(self, name, description, skill_type, portion_type, materials):
        super().type_text_in_input('.modal.fade.in #id_activity_name', name)
        super().type_text_in_input('.modal.fade.in #id_description', description)
        super().type_text_in_input('.modal.fade.in #id_materials', materials)
        super().choose_option_from_select('id_activity_skill_type', skill_type)
        super().choose_option_from_select('id_activity_portion_type', portion_type)
        super().click_modal_save_button()
        time.sleep(PAGE_LOADING_WAIT_TIME)

    def __add_generic_activity(self, name, description, skill_type, portion_type, materials):
        super().click_button('add-generic-activity')
        time.sleep(MODAL_TRANSITION_WAIT_TIME)
        self.__fill_generic_activity_fields(name, description, skill_type, portion_type, materials)

    def __edit_first_generic_activity(self, name, description, skill_type, portion_type, materials, old_portion_type=None):
        edit_button = self.browser.find_element_by_css_selector('.page-subsubheader-right > .btn-primary')
        edit_button.click()
        time.sleep(MODAL_TRANSITION_WAIT_TIME)
        if old_portion_type is not None:
            self.__assert_portion_type_dropdown_value(old_portion_type)
        self.__fill_generic_activity_fields(name, description, skill_type, portion_type, materials)

    # Assertions
    def __assert_generic_activity_existence(self, name, description, skill_type, portion_type, materials):
        self.assertTrue(Activity.objects.filter(lesson=None, activity_name=name, description=description, activity_skill_type=skill_type, activity_portion_type=portion_type, materials=materials).exists())
        content = self.browser.find_element_by_id('paw-main-content').text
        self.assertIn(name, content)
        self.assertIn(materials, content)

    def __assert_portion_type_dropdown_value(self, expected_value):
        selected_value = self.browser.find_element_by_css_selector('.modal.fade.in #id_activity_portion_type > option:checked').text
        self.assertEqual(selected_value, expected_value)

    # Tests
    # python3 manage.py test lessons.test_manage_generic_activity.GenericActivityManagementTestCases.test_add_generic_activity
    def test_add_generic_activity(self):
        name = 'Hello Song'
        description = 'Hello, hello, hello, how are you? I\'m fine, I\'m fine. I\'m fine, thank you, and you?'
        name_skill_type = NAME_VOCABULARY
        name_portion_type = NAME_GREETING
        skill_type = VOCABULARY
        portion_type = GREETING
        materials = 'CD'
        super().go_to_generic_activities_page()
        self.__add_generic_activity(name, description, name_skill_type, name_portion_type, materials)
        self.__assert_generic_activity_existence(name, description, skill_type, portion_type, materials)

    def test_edit_generic_activity(self):
        name = 'Hello, Hello, What\'s Your Name?'
        description = 'Hello, hello, what\'s your name? What\'s your name? What\'s your name? Hello, hello, what\'s your name? My name\'s Makoto'
        name_skill_type = NAME_CONVERSATION
        name_portion_type = NAME_WARMUP
        skill_type = CONVERSATION
        portion_type = WARMUP
        materials = 'Name tags, CD'
        super().go_to_generic_activities_page_with_a_generic_activity()
        self.__edit_first_generic_activity(name, description, name_skill_type, name_portion_type, materials, NAME_GREETING)
        self.__assert_generic_activity_existence(name, description, skill_type, portion_type, materials)

