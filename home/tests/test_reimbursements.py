import time, os
import selenium
from lessons.models import *
from paw.constants.tests import *
from paw.constants.models import *
from lessons.constants import *
from datetime import datetime, timedelta
from selenium.webdriver.common.keys import Keys
from home.tests.tests import HomeTestMethods

class ReimbursementTestCases(HomeTestMethods):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    # Actions
    def __click_view_reimbursements_button(self):
        button = self.browser.find_element_by_class_name('btn-view-reimbursements')
        button.click()
        time.sleep(PAGE_LOADING_WAIT_TIME)

    def __toggle_reimbursement_switch(self):
        self.browser.execute_script("$('table .bootstrap-switch input').first().click();")
        time.sleep(BOOTSTRAP_SWITCH_TRANSITION_WAIT_TIME)

    def __click_generate_code_button(self):
        self.browser.find_element_by_id('reimbursement-code-generation-button').click()
        time.sleep(MODAL_TRANSITION_WAIT_TIME)

    def __add_reimbursement_item(self, date, route_name):
        super().type_text_in_input('#add-reimbursement-date', date)
        self.browser.find_element_by_id('paw-main-content').click()
        super().choose_option_from_select('add-reimbursement-route', route_name, is_modal=False)
        self.browser.find_element_by_id('add-new-route').click()

    # Assertions
    def __assert_reimbursements_page(self, total_cost, expected_text):
        content = self.browser.find_element_by_id('paw-main-content').text
        self.assertIn('Total: ￥%d'%(total_cost), content)
        self.assertIn('%s'%(expected_text), content)

    # Tests
    # python3 manage.py test home.tests.test_reimbursements.ReimbursementTestCases.test_no_school_years
    def test_no_school_years(self):
        super().go_to_reimbursements_page()
        super().assert_no_school_years()

    def test_view_reimbursements(self):
        super().go_to_reimbursements_page_with_complete_package()
        self.__click_view_reimbursements_button()
        self.__assert_reimbursements_page(total_cost=500, expected_text='%s Dolphin Elementary School 500'%(datetime.now().strftime('%Y-%m-%d')))

    def test_toggle_include_option(self):
        super().go_to_reimbursements_page_with_complete_package()
        self.__click_view_reimbursements_button()
        self.__toggle_reimbursement_switch()
        self.__assert_reimbursements_page(total_cost=0, expected_text='%s Dolphin Elementary School 500'%(datetime.now().strftime('%Y-%m-%d')))

    def test_generate_code(self):
        super().go_to_reimbursements_page_with_complete_package()
        self.__click_view_reimbursements_button()
        self.__click_generate_code_button()
        content = self.browser.find_element_by_css_selector('.modal.fade.in').text
        self.assertIn('all_routes.push({\n "dates": [\'%s\'],\n "destination": \'Dolphin Elementary School\',\n "from": \'Dolphino Station\',\n "to": \'Dolphin Elementary School Bus Stop\',\n "method": \'01.Not Selected\',\n "isRoundTrip": true,\n "fee": 500,\n});'%(datetime.now().strftime('%d')), content)

    def test_add_reimbursement_item(self):
        date = datetime.now().strftime('%Y-%m-%d')
        super().go_to_reimbursements_page_with_school()
        self.__click_view_reimbursements_button()
        self.__add_reimbursement_item(date, 'Dolphin Elementary School')
        self.__assert_reimbursements_page(total_cost=500, expected_text='%s Dolphin Elementary School 500'%(date))

    def test_add_reimbursement_item_and_toggle_it(self):
        date = datetime.now().strftime('%Y-%m-%d')
        super().go_to_reimbursements_page_with_school()
        self.__click_view_reimbursements_button()
        self.__add_reimbursement_item(date, 'Dolphin Elementary School')
        self.__toggle_reimbursement_switch()
        self.__assert_reimbursements_page(total_cost=0, expected_text='%s Dolphin Elementary School 500'%(datetime.now().strftime('%Y-%m-%d')))

    def test_add_item_button(self):
        super().go_to_reimbursements_page_with_school()
        self.__click_view_reimbursements_button()
        self.browser.find_element_by_id('add-reimbursement-entry-button').click()
        self.assertEqual(self.browser.find_element_by_id('add-reimbursement-date'), self.browser.switch_to.active_element)

    def test_alt_meeting_reimbursement_item(self):
        date = datetime.now().strftime('%Y-%m-%d')
        super().go_to_reimbursements_page_with_alt_meeting()
        self.__click_view_reimbursements_button()
        self.__assert_reimbursements_page(total_cost=870, expected_text='%s Route to and from ALT Meeting 870'%(date))
        