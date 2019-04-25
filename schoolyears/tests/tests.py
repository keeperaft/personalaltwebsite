import time
import selenium
from selenium import webdriver
from django.contrib.auth.models import User
from schoolyears.models import *
from paw.constants.tests import *
from datetime import datetime, timedelta
from django.test import Client
from selenium.webdriver.common.keys import Keys
from schoolyears.constants import BLUE

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class SchoolYearTestMethods(StaticLiveServerTestCase):

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

    # Go to certain pages
    def go_to_school_year_page(self):
        self.browser.get('%s%s' % (self.live_server_url, '/schoolyears/'))

    def go_to_school_year_page_with_existing_school_year(self):
        start_date = datetime.strptime('2017-04-15', '%Y-%m-%d')
        end_date = datetime.strptime('2018-03-25', '%Y-%m-%d')
        new_entry = SchoolYear(
            name = '2017 ~ 2018',
            start_date = start_date,
            end_date = end_date,
            is_active = False
        )
        new_entry.save()
        self.browser.get('%s%s' % (self.live_server_url, '/schoolyears/'))

    def go_to_school_year_page_with_existing_school_year_and_school(self):
        start_date = datetime.strptime('2017-04-15', '%Y-%m-%d')
        end_date = datetime.strptime('2018-03-25', '%Y-%m-%d')
        new_school_year_entry = SchoolYear(
            name = '2017 ~ 2018',
            start_date = start_date,
            end_date = end_date,
            is_active = False
        )
        new_school_year_entry.save()
        new_school_entry = School(
            school_colors=BLUE,
            school_type=HIGH_SCHOOL,
            school_year=new_school_year_entry,
            name='School of Hope',
            name_kanji='希望の高校',
            address='123-4567 Test, Setagaya-ku, Tokyo, Japan',
            contact_number='080-1234-5678',
            website='http://example.com',
            principal='Makoto Naegi',
            vice_principal='Hajime Hinata',
            english_head_teacher='Kaede Akamatsu'
        )
        new_school_entry.save()
        self.browser.get('%s%s' % (self.live_server_url, '/schoolyears/'))
        time.sleep(PAGE_LOADING_WAIT_TIME)

    # User actions
    def click_button(self, button_name):
        self.browser.execute_script("$('button[name="+button_name+"]').click()")

    def click_a_tag(self, tag_id):
        element = self.browser.find_element_by_id(tag_id)
        element.click()

    def click_modal_save_button(self):
        self.browser.execute_script("$('.modal.fade.in .modal-footer .btn-primary').click();")
        time.sleep(PAGE_LOADING_WAIT_TIME)

    def type_text_in_input(self, css_selector, input_text):
        element = self.browser.find_element_by_css_selector(css_selector)
        element.clear()
        element.click()
        element.send_keys(input_text)

    # Adding a new school year: used in both SchoolYearManagingTestCases and SchoolManagingTestCases
    def add_school_year(self):
        self.go_to_school_year_page()
        self.browser.find_element_by_link_text('+ Add New School Year').click()
        time.sleep(MODAL_TRANSITION_WAIT_TIME)

    def add_school_year_start_date(self, input_text):
        self.type_text_in_input('.modal.fade.in #id_start_date', input_text)

    def add_school_year_end_date(self, input_text):
        self.type_text_in_input('.modal.fade.in #id_end_date', input_text)

    def add_school_year_save(self):
        self.click_modal_save_button()
        time.sleep(PAGE_LOADING_WAIT_TIME)

    def save_new_school_year(self, start_date, end_date):
        self.add_school_year()
        self.add_school_year_start_date(start_date)
        self.add_school_year_end_date(end_date)
        self.add_school_year_save()

    # Assertions
    def assert_success_message(self, success_message):
        element = self.browser.find_element_by_css_selector('#paw-messages .alert-success')
        success_message = '\xd7\n'+str(success_message)
        self.assertEqual(element.text, success_message)

    def assert_modal_error_message(self, error_message):
        element = self.browser.find_element_by_css_selector('.modal.fade.in .alert-danger')
        error_message = '\xd7\nError: '+str(error_message)
        element_text = element.text.strip()
        self.assertEqual(element_text, error_message)
        