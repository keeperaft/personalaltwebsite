import time
from schoolyears.models import *
from paw.constants.tests import *
from schoolyears.constants import *
from datetime import datetime, timedelta
from schoolyears.tests.tests import SchoolYearTestMethods

class SchoolYearManagingTestCases(SchoolYearTestMethods):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def __assert_school_year_exists(self, school_year_name, school_year_duration):
        # Check if it exists in database
        self.assertTrue(SchoolYear.objects.filter(name=school_year_name).exists())

        # Confirm that the newly added element is there
        sidebar = self.browser.find_element_by_id('paw-sidebar')
        self.assertIn(school_year_name, sidebar.text)

        content = self.browser.find_element_by_id('paw-main-content')
        self.assertIn(school_year_name, content.text)
        self.assertIn(school_year_duration, content.text)

        super().assert_success_message(MSG_SUCCESS_NEW_SCHOOLYEAR)

    ###################
    # Add school year #
    ###################

    # To run a single test case:
    # python manage.py test schoolyears.tests.SchoolYearTestCases.test_add_school_year_normal
    def test_add_school_year_normal(self):
        super().save_new_school_year('2017-04-15', '2018-03-31')
        time.sleep(PAGE_LOADING_WAIT_TIME)
        self.__assert_school_year_exists('2017 ~ 2018', 'April 15, 2017 ~ March 31, 2018')

    def test_add_school_year_same_year_different_months(self):
        super().save_new_school_year('2016-04-10', '2016-07-30')
        time.sleep(PAGE_LOADING_WAIT_TIME)
        self.__assert_school_year_exists('Apr ~ Jul 2016', 'April 10, 2016 ~ July 30, 2016')

    def test_add_school_year_active_school_year(self):
        current_date = datetime.now()
        prev_date = current_date - timedelta(days=5)
        next_date = current_date + timedelta(days=5)

        super().save_new_school_year(
            prev_date.strftime('%Y-%m-%d'), 
            next_date.strftime('%Y-%m-%d'))

        time.sleep(PAGE_LOADING_WAIT_TIME)
        content = self.browser.find_element_by_id('paw-main-content')
        self.assertIn('This school year is the active school year.', content.text)

    def test_add_school_year_inactive_school_year(self):
        super().save_new_school_year('2000-01-01', '2001-01-01')
        time.sleep(PAGE_LOADING_WAIT_TIME)
        content = self.browser.find_element_by_id('paw-main-content')
        self.assertIn('This school year is inactive.', content.text)

    def test_add_school_year_from_content_button(self):
        super().go_to_school_year_page()
        super().click_a_tag('add-school-year-from-content')
        time.sleep(MODAL_TRANSITION_WAIT_TIME)
        super().add_school_year_start_date('2017-04-15')
        super().add_school_year_end_date('2018-03-31')
        super().add_school_year_save()
        time.sleep(PAGE_LOADING_WAIT_TIME)
        self.__assert_school_year_exists('2017 ~ 2018', 'April 15, 2017 ~ March 31, 2018')
        super().assert_success_message(MSG_SUCCESS_NEW_SCHOOLYEAR)

    def test_add_school_year_from_datepicker(self):
        super().go_to_school_year_page()
        super().add_school_year()
        time.sleep(MODAL_TRANSITION_WAIT_TIME)
        
        element = self.browser.find_element_by_id('id_start_date')
        element.click()
        element = self.browser.find_element_by_css_selector('.datepicker-days .old')
        element.click()
        element = self.browser.find_element_by_id('id_end_date')
        element.click()
        element = self.browser.find_element_by_css_selector('.datepicker-days .next')
        element.click()
        element = self.browser.find_element_by_css_selector('.datepicker-days .day')
        element.click()

        super().add_school_year_save()
        time.sleep(PAGE_LOADING_WAIT_TIME)

        # Check if it exists in database
        self.assertEqual(SchoolYear.objects.all().count(), 1)

    def test_add_school_year_end_earlier_than_start(self):
        super().save_new_school_year('2015-01-01', '2013-01-01')
        content = self.browser.find_element_by_id('paw-main-content')
        self.assertIn('End Date: End date must be later than Start date.', content.text)
        
    ####################
    # Edit school year #
    ####################

    def test_edit_school_year(self):
        super().go_to_school_year_page_with_existing_school_year()
        content = self.browser.find_element_by_id('paw-main-content')
        self.assertIn('April 15, 2017 ~ March 25, 2018', content.text)

        super().click_button('edit-school-year')
        time.sleep(MODAL_TRANSITION_WAIT_TIME)
        super().add_school_year_start_date('2017-04-25')
        super().add_school_year_end_date('2018-02-27')
        super().click_modal_save_button()

        time.sleep(PAGE_LOADING_WAIT_TIME)
        content = self.browser.find_element_by_id('paw-main-content')
        self.assertIn('April 25, 2017 ~ Feb. 27, 2018', content.text)
        super().assert_success_message(MSG_SUCCESS_EDIT_SCHOOLYEAR)
    