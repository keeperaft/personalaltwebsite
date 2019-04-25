import time, os
import selenium
from lessons.models import *
from paw.constants.tests import *
from paw.constants.models import *
from lessons.constants import *
from datetime import datetime, timedelta
from selenium.webdriver.common.keys import Keys
from home.tests.tests import HomeTestMethods

class SettingsTestCases(HomeTestMethods):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    # Tests
    # python3 manage.py test home.tests.test_settings.SettingsTestCases.test_change_password
    def test_change_password(self):
        super().go_to_settings_page()
        super().type_text_in_input('#id_old_password', 'testpassword')
        super().type_text_in_input('#id_new_password1', 'testnewpassword')
        super().type_text_in_input('#id_new_password2', 'testnewpassword')
        self.browser.find_element_by_class_name('btn-primary').click()
        time.sleep(PAGE_LOADING_WAIT_TIME)

        self.browser.find_element_by_id('logout-link').click()
        time.sleep(PAGE_LOADING_WAIT_TIME)
        
        super().type_text_in_input('#id_username', 'tester')
        super().type_text_in_input('#id_password', 'testnewpassword')
        self.browser.find_element_by_class_name('btn-primary').click()
        time.sleep(PAGE_LOADING_WAIT_TIME)

        content = self.browser.find_element_by_css_selector('body')
        self.assertIn('Login successful. Welcome back!', content.text)
    