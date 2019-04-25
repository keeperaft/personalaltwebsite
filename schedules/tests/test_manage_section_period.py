import time, os
import selenium
from schedules.models import *
from paw.constants.tests import *
from paw.constants.models import *
from schedules.constants import *
from datetime import datetime, timedelta
from selenium.webdriver.common.keys import Keys
from schedules.tests.tests import ScheduleTestMethods

class SectionPeriodManagementTestCases(ScheduleTestMethods):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    # Actions
    def __click_view_profile(self):
        link = self.browser.find_element_by_id('view-school-profile-button')
        link.click()
        time.sleep(PAGE_LOADING_WAIT_TIME)

    def __click_junior_high_school_view_year_profile(self):
        super().choose_option_from_select('select_school', 'Shark Junior High School', is_modal=False)
        self.__click_view_profile()

    def __add_normal_day_period(self, start_time, end_time):
        super().type_text_in_input('.start-time', start_time)
        super().type_text_in_input('.end-time', end_time)
        self.browser.find_element_by_class_name('btn-add-new-time-period').click()

    def __delete_time_period(self, period_number):
        button = self.browser.find_element_by_css_selector('tr:nth-child(%d) .delete-time-period-button'%(period_number+1))
        button.click()
        time.sleep(MODAL_TRANSITION_WAIT_TIME)

    def __enter_text_in_editable_field(self, value):
        editable_field_element = self.browser.find_element_by_id('editable-field')
        editable_field_element.click()
        editable_field_element.clear()
        editable_field_element.send_keys(value)

        done_button_element = self.browser.find_element_by_id('done-button')
        done_button_element.click()

    def __edit_time_period(self, period_number, new_start_time, new_end_time):
        editable_label = self.browser.find_element_by_css_selector('tr:nth-child(%d) td:nth-child(2) > .editable-label'%(period_number+1))
        editable_label.click()
        self.__enter_text_in_editable_field(new_start_time)

        editable_label = self.browser.find_element_by_css_selector('tr:nth-child(%d) td:nth-child(3) > .editable-label'%(period_number+1))
        editable_label.click()
        self.__enter_text_in_editable_field(new_end_time)

    def __fill_modal_profile(self, profile_name, profile_type):
        super().type_text_in_input('.modal.fade.in #id_period_name', profile_name)
        super().choose_option_from_select('id_period_type', profile_type, is_modal=True)
        super().click_modal_save_button()
        time.sleep(PAGE_LOADING_WAIT_TIME)

    def __add_new_profile(self, profile_name, profile_type):
        super().click_button('add-period-profile-entry-button')
        time.sleep(MODAL_TRANSITION_WAIT_TIME)
        self.__fill_modal_profile(profile_name, profile_type)

    def __edit_profile(self, profile_name, profile_type):
        button = self.browser.find_element_by_class_name('edit-period-profile-entry-button')
        button.click()
        time.sleep(MODAL_TRANSITION_WAIT_TIME)
        self.__fill_modal_profile(profile_name, profile_type)

    # Assertions
    def __assert_profile_existence(self, profile_name, profile_description):
        content = self.browser.find_element_by_id('paw-main-content').text
        self.assertIn('%s %s'%(profile_name, profile_description), content)

    def __assert_elementary_school_period_profiles(self):
        content = self.browser.find_element_by_id('paw-main-content').text
        self.assertIn('Normal Schedule Normal days', content)
        self.assertIn('Monday Schedule Mondays', content)
        self.assertIn('Wednesday Schedule Wednesdays', content)

    def __assert_junior_high_school_period_profiles(self):
        content = self.browser.find_element_by_id('paw-main-content').text
        self.assertIn('Normal Schedule Normal days', content)

    def __assert_time_period_existence(self, period, start_time, end_time):
        content = self.browser.find_element_by_class_name('period-display-table').text
        self.assertIn('%s %s %s'%(period, start_time, end_time), content)

    def __assert_time_period_inexistence(self, period, start_time, end_time):
        content = self.browser.find_element_by_class_name('period-display-table').text
        self.assertNotIn('%s %s %s'%(period, start_time, end_time), content)

    # Tests
    # python3 manage.py test schedules.tests.test_manage_section_period.SectionPeriodManagementTestCases.test_no_school_years_available
    def test_no_school_years_available(self):
        super().go_to_school_periods_page()
        super().assert_no_school_years()

    def test_no_schools_available(self):
        super().go_to_school_periods_page_with_school_year()
        super().assert_dropdown_enabled('select[name="school-year"]', True)
        super().assert_dropdown_enabled('select[name="school"]', False)

    def test_elementary_school_schedule(self):
        super().go_to_school_periods_with_school()
        self.__click_view_profile()
        self.__assert_elementary_school_period_profiles()

    def test_junior_high_school_schedule(self):
        super().go_to_school_periods_with_school()
        self.__click_junior_high_school_view_year_profile()
        self.__assert_junior_high_school_period_profiles()

    def test_add_time_period(self):
        period = '7'
        start_time = '16:15'
        end_time = '17:23'
        super().go_to_school_periods_with_school()
        self.__click_view_profile()
        self.__add_normal_day_period(start_time, end_time)
        self.__assert_time_period_existence(period, start_time, end_time)

    def test_add_time_period_incorrect_format(self):
        period = '7'
        start_time = '1615'
        end_time = '17.23'
        super().go_to_school_periods_with_school()
        self.__click_view_profile()
        self.__add_normal_day_period(start_time, end_time)
        self.__assert_time_period_inexistence(period, start_time, end_time)
    
    def test_delete_time_period(self):
        super().go_to_school_periods_with_school()
        self.__click_view_profile()
        self.__delete_time_period(3)
        self.__assert_time_period_existence('1', '08:50', '09:35')
        self.__assert_time_period_existence('2', '09:40', '10:25')
        self.__assert_time_period_existence('3', '11:35', '12:20')
        self.__assert_time_period_existence('4', '13:50', '14:35')
        self.__assert_time_period_existence('5', '14:40', '15:25')
        self.__assert_time_period_inexistence('3', '10:45', '11:30')
    
    def test_edit_time_period(self):
        super().go_to_school_periods_with_school()
        self.__click_view_profile()
        self.__edit_time_period(2, '9:45', '10:30')
        self.__assert_time_period_existence('2', '9:45', '10:30')
    
    def test_new_period_profile(self):
        profile_name = 'A4 Schedule'
        profile_type = 'Special days'
        super().go_to_school_periods_with_school()
        self.__click_view_profile()
        self.__add_new_profile(profile_name, profile_type)
        self.__assert_profile_existence(profile_name, profile_type)
    
    def test_edit_period_profile(self):
        profile_name = 'Default Schedule'
        profile_type = 'Normal days'
        super().go_to_school_periods_with_school()
        self.__click_view_profile()
        self.__edit_profile(profile_name, profile_type)
        self.__assert_profile_existence(profile_name, profile_type)

        
