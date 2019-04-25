import time, os
import selenium
from lessons.models import *
from paw.constants.tests import *
from paw.constants.models import *
from lessons.constants import *
from datetime import datetime, timedelta
from selenium.webdriver.common.keys import Keys
from home.tests.tests import HomeTestMethods

class TimesheetTestCases(HomeTestMethods):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    # Actions
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

    # Assertions

    # Tests
    # python3 manage.py test home.tests.test_timesheet.TimesheetTestCases.test_no_school_years
    def test_no_school_years(self):
        super().go_to_timesheets_page()
        super().assert_no_school_years()

    def test_no_schools(self):
        super().go_to_timesheets_page_with_school_year()
        super().assert_enabled('select[name="school-year"]', True)
        super().assert_enabled('select[name="school"]', False)
        super().assert_enabled('.btn-generate-pdf', False)

    def test_print_month(self):
        super().go_to_timesheets_page_with_school()
        super().choose_option_from_select(selector_id='school-dropdown', option_text='Dolphin Elementary School', is_modal=False)
        self.browser.find_element_by_class_name('btn-generate-pdf').click()
        super().assert_download_did_not_fail()
