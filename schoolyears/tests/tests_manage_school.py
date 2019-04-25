import time
import selenium
from schoolyears.models import *
from paw.constants.tests import *
from schoolyears.constants import *
from datetime import datetime, timedelta
from selenium.webdriver.common.keys import Keys
from schoolyears.tests.tests import SchoolYearTestMethods

class SchoolManagingTestCases(SchoolYearTestMethods):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    ##############
    # Add school #
    ############## 

    FIELD_NAME = 0
    FIELD_NAME_KANJI = 1
    FIELD_ADDRESS = 2
    FIELD_CONTACT_NUMBER = 3
    FIELD_WEBSITE = 4
    FIELD_PRINCIPAL = 5
    FIELD_VICE_PRINCIPAL = 6
    FIELD_ENGLISH_HEAD_TEACHER = 7

    def __add_school_select_school_type(self, school_type_tuple):
        index = str(SCHOOL_TYPES.index(school_type_tuple) + 1)
        element = self.browser.find_element_by_css_selector('#id_school_type')
        element.click()
        element = self.browser.find_element_by_css_selector('#id_school_type > option:nth-child('+index+')')
        element.click()
        element = self.browser.find_element_by_css_selector('#id_school_type')
        element.click()
        
    def __add_school_name(self, name):
        super().type_text_in_input('.modal.fade.in #id_name', name)

    def __add_school_kanji(self, kanji_name):
        super().type_text_in_input('.modal.fade.in #id_name_kanji', kanji_name)

    def __add_school(self, school_name, kanji_name, school_type_tuple):
        super().click_button('add-school-button')
        time.sleep(MODAL_TRANSITION_WAIT_TIME)
        self.__add_school_name(school_name)
        self.__add_school_kanji(kanji_name)
        self.__add_school_select_school_type(school_type_tuple)
        super().click_modal_save_button()

    def __click_show_button_of_first_school_in_page(self):
        show_button = self.browser.find_element_by_class_name('toggle-visibility')
        if show_button.text == 'Show':
            show_button.click()

    def __click_editable_label_of_school_field(self, school_field_type):
        editable_label_elements = self.browser.find_elements_by_class_name('editable-label')
        field_element = editable_label_elements[school_field_type]
        field_element.click()

    def __enter_text_in_editable_field(self, value):
        editable_field_element = self.browser.find_element_by_id('editable-field')
        editable_field_element.click()
        editable_field_element.clear()
        editable_field_element.send_keys(value)

    def __edit_one_school_field(self, school_field_type, value):
        self.__click_show_button_of_first_school_in_page()

        # Edit the new school
        self.__click_editable_label_of_school_field(school_field_type)
        self.__enter_text_in_editable_field(value)

        done_button_element = self.browser.find_element_by_id('done-button')
        done_button_element.click()

    def __assert_one_school_field(self, school_field_type, value):
        show_button = self.browser.find_element_by_class_name('toggle-visibility')
        if show_button.text == 'Show':
            show_button.click()

        editable_label_elements = self.browser.find_elements_by_class_name('editable-label')
        self.assertEqual(value, editable_label_elements[school_field_type].text)

    def __assert_school_existence(self, school_name, kanji_name, school_type, school_color):
        # Check if it exists in database
        self.assertTrue(School.objects.filter(name=school_name).exists())

        # Reload the page and confirm that the newly added element is there
        editable_label_elements = self.browser.find_elements_by_class_name('editable-label')
        self.assertEqual(school_name, editable_label_elements[0].text)
        self.assertEqual(kanji_name, editable_label_elements[1].text)

        # Check if the default color is being entered
        # NOTE: If the default school color is changed, please update this test
        time.sleep(2)
        school_color_element = self.browser.find_element_by_class_name('school-color')
        self.assertEqual(school_color_element.value_of_css_property('background-color'), school_color)

        show_button = self.browser.find_element_by_class_name('toggle-visibility')
        show_button.click()

        school_type_element = self.browser.find_element_by_class_name('editable-dropdown')
        self.assertEqual(school_type[1], school_type_element.text)

        super().assert_success_message(MSG_SUCCESS_NEW_SCHOOL)

    def __assert_school_details_of_first_school_in_page(self, 
        school_type_tuple, name, name_kanji, address, contact_number, 
        website, principal, vice_principal, english_head_teacher):

        # Note! Must obey the order found in the school years page
        school_details = [name, name_kanji, address, contact_number, website, principal,
            vice_principal, english_head_teacher]

        show_button = self.browser.find_element_by_class_name('toggle-visibility')
        show_button.click()

        editable_label_elements = self.browser.find_elements_by_class_name('editable-label')

        # Check the school details
        for i in range(len(school_details)):
            self.assertEqual(school_details[i], editable_label_elements[i].text)

        # Check the type of school
        school_type_element = self.browser.find_element_by_class_name('editable-dropdown')
        self.assertEqual(school_type_tuple[1], school_type_element.text)

    def __change_editable_text_of_first_school_in_page(self, 
        school_type_tuple, name, name_kanji, address, contact_number, 
        website, principal, vice_principal, english_head_teacher):

        # Note! Must obey the order found in the school years page
        school_details = [name, name_kanji, address, contact_number, website, principal,
            vice_principal, english_head_teacher]

        show_button = self.browser.find_element_by_class_name('toggle-visibility')
        show_button.click()

        editable_label_elements = self.browser.find_elements_by_class_name('editable-label')

        for i in range(len(school_details)):
            editable_label_element = editable_label_elements[i]
            editable_label_element.click()

            editable_field_element = self.browser.find_element_by_id('editable-field')
            editable_field_element.click()
            editable_field_element.clear()
            editable_field_element.send_keys(school_details[i])

            done_button_element = self.browser.find_element_by_id('done-button')
            done_button_element.click()

        # Check the type of school
        school_type_element = self.browser.find_element_by_class_name('editable-dropdown')
        school_type_element.click()

        index = str(SCHOOL_TYPES.index(school_type_tuple) + 1)
        editable_field_element = self.browser.find_element_by_id('editable-field')
        editable_field_element.click()

        element = self.browser.find_element_by_css_selector('#editable-field > option:nth-child('+index+')')
        element.click()
        element = self.browser.find_element_by_css_selector('#editable-field')
        element.click()
        done_button_element = self.browser.find_element_by_id('done-button')
        done_button_element.click()


    def test_add_school(self):
        school_name = 'Tana ES'
        kanji_name = '田名小学校'
        school_type = (ELEMENTARY_SCHOOL, NAME_ELEMENTARY_SCHOOL)
        school_color = 'rgb(151, 255, 173)' # NOTE: If the default school color is changed, please update this test

        super().go_to_school_year_page_with_existing_school_year()
        self.__add_school(school_name, kanji_name, school_type)
        self.__assert_school_existence(school_name, kanji_name, school_type, school_color)

    def test_add_school_from_content_button(self):
        school_name = 'Oosawa JHS'
        kanji_name = '大沢中学校'
        school_type = (JUNIOR_HIGH_SCHOOL, NAME_JUNIOR_HIGH_SCHOOL)
        school_color = 'rgb(151, 255, 173)' # NOTE: If the default school color is changed, please update this test

        super().go_to_school_year_page_with_existing_school_year()
        super().click_a_tag('add-school-from-content')
        self.__add_school_name(school_name)
        self.__add_school_kanji(kanji_name)
        self.__add_school_select_school_type(school_type)
        super().click_modal_save_button()

        self.__assert_school_existence(school_name, kanji_name, school_type, school_color)

    def test_add_school_trimmable_names(self):
        school_name = '         Yumenooka HS    '
        kanji_name = '   夢の丘高校   '
        school_name_trimmed = 'Yumenooka HS'
        kanji_name_trimmed = '夢の丘高校'
        school_type = (HIGH_SCHOOL, NAME_HIGH_SCHOOL)
        school_color = 'rgb(151, 255, 173)' # NOTE: If the default school color is changed, please update this test

        super().go_to_school_year_page_with_existing_school_year()
        self.__add_school(school_name, kanji_name, school_type)
        self.__assert_school_existence(school_name_trimmed, kanji_name_trimmed, school_type, school_color)

    def test_add_school_spaces_only(self):
        school_name = '　　　　　'
        kanji_name = '　　　　　　　'
        school_type = (ELEMENTARY_SCHOOL, NAME_ELEMENTARY_SCHOOL)

        super().go_to_school_year_page_with_existing_school_year()
        self.__add_school(school_name, kanji_name, school_type)

        modal_element = self.browser.find_element_by_css_selector('.modal.fade.in')
        self.assertIn(str(MSG_ERR_ADD_SCHOOL), modal_element.text)

    def test_add_school_spaces_only_check_other_modals(self):
        self.test_add_school_spaces_only()
        modal_close_element = self.browser.find_element_by_css_selector('.modal.fade.in .close')
        modal_close_element.click()
        time.sleep(MODAL_TRANSITION_WAIT_TIME)

        self.browser.find_element_by_link_text('+ Add New School Year').click()
        time.sleep(MODAL_TRANSITION_WAIT_TIME)

        modal_element = self.browser.find_element_by_css_selector('.modal.fade.in')
        self.assertNotIn(str(MSG_ERR_ADD_SCHOOL), modal_element.text)

    # The ultimate school addition test case -- 45 seconds
    # This test produces inconsistent results.
    def inconsistent_test_add_edit_school_existing_school_information(self):
        super().go_to_school_year_page_with_existing_school_year_and_school()
        super().save_new_school_year('2018-04-15', '2019-03-31')
        
        # Click new schoolyear
        element = self.browser.find_element_by_link_text('2018 ~ 2019')
        element.click()
        time.sleep(MODAL_TRANSITION_WAIT_TIME)

        # Add new school
        school_name = 'School of Hope'
        kanji_name = '希望の高校'
        school_type = (HIGH_SCHOOL, NAME_HIGH_SCHOOL)
        self.__add_school(school_name, kanji_name, school_type)

        # Confirm that it has the same details
        self.__assert_school_details_of_first_school_in_page(
            school_type_tuple=(HIGH_SCHOOL, NAME_HIGH_SCHOOL),
            name='School of Hope',
            name_kanji='希望の高校',
            address='123-4567 Test, Setagaya-ku, Tokyo, Japan',
            contact_number='080-1234-5678',
            website='http://example.com',
            principal='Makoto Naegi',
            vice_principal='Hajime Hinata',
            english_head_teacher='Kaede Akamatsu')

        # Edit the new school
        new_contact_number = '080-3141-5926'
        self.__edit_one_school_field(self.FIELD_CONTACT_NUMBER, new_contact_number)

        # Add a new school year
        super().save_new_school_year('2019-04-15', '2020-03-31')
        
        # Click new schoolyear
        element = self.browser.find_element_by_link_text('2019 ~ 2020')
        element.click()
        time.sleep(MODAL_TRANSITION_WAIT_TIME)

        # Add new school
        school_name = 'School of Hope'
        kanji_name = '希望の高校'
        school_type = (HIGH_SCHOOL, NAME_HIGH_SCHOOL)
        self.__add_school(school_name, kanji_name, school_type)

        # Confirm that it has the same details
        self.__assert_school_details_of_first_school_in_page(
            school_type_tuple=(HIGH_SCHOOL, NAME_HIGH_SCHOOL),
            name='School of Hope',
            name_kanji='希望の高校',
            address='123-4567 Test, Setagaya-ku, Tokyo, Japan',
            contact_number=new_contact_number,
            website='http://example.com',
            principal='Makoto Naegi',
            vice_principal='Hajime Hinata',
            english_head_teacher='Kaede Akamatsu')

    ###############
    # Edit School #
    ###############
    # This test produces inconsistent results.
    def inconsistent_test_edit_school_edit_all_fields(self):
        new_school_type_tuple = (JUNIOR_HIGH_SCHOOL, NAME_JUNIOR_HIGH_SCHOOL)
        new_name = 'Despair Junior High School'
        new_name_kanji = '絶望の中学校'
        new_address = '242-0568 Test, Meguro-ku, Tokyo, 1-23-45'
        new_contact_number = '080-1470-3690'
        new_website = 'http://desp-example.com'
        new_principal = 'Junko Enoshima'
        new_vice_principal = 'Mukuro Ikusaba'
        new_english_head_teacher = 'Nagito Komaeda'

        super().go_to_school_year_page_with_existing_school_year_and_school()
        self.__change_editable_text_of_first_school_in_page(
            school_type_tuple=new_school_type_tuple, 
            name=new_name, 
            name_kanji=new_name_kanji, 
            address=new_address, 
            contact_number=new_contact_number, 
            website=new_website, 
            principal=new_principal, 
            vice_principal=new_vice_principal, 
            english_head_teacher=new_english_head_teacher)

        super().go_to_school_year_page()
        self.__assert_school_details_of_first_school_in_page(
            school_type_tuple=new_school_type_tuple, 
            name=new_name, 
            name_kanji=new_name_kanji, 
            address=new_address, 
            contact_number=new_contact_number, 
            website=new_website, 
            principal=new_principal, 
            vice_principal=new_vice_principal, 
            english_head_teacher=new_english_head_teacher)

    def test_edit_school_empty_one_field(self):
        super().go_to_school_year_page_with_existing_school_year_and_school()
        self.__edit_one_school_field(self.FIELD_WEBSITE, '')
        self.__assert_one_school_field(self.FIELD_WEBSITE, 'N/A')

    def test_edit_school_cancel_one_field(self):
        super().go_to_school_year_page_with_existing_school_year_and_school()
        show_button = self.browser.find_element_by_class_name('toggle-visibility')
        if show_button.text == 'Show':
            show_button.click()

        # Edit the new school
        self.__click_editable_label_of_school_field(self.FIELD_PRINCIPAL)
        self.__enter_text_in_editable_field('')
        cancel_button_element = self.browser.find_element_by_id('cancel-button')
        cancel_button_element.click()

        self.__assert_one_school_field(self.FIELD_PRINCIPAL, 'Makoto Naegi')

    def test_edit_school_change_school_color(self):
        super().go_to_school_year_page_with_existing_school_year_and_school()
        self.browser.execute_script("$('.school-color').click()")

        # Note: Please change this test case if the color for blue was changed.
        school_color_choices = self.browser.find_elements_by_css_selector('.modal.fade.in .school-color')
        school_color_choices[2].click() # Blue, rgb(63, 192, 255)
        self.browser.execute_script("$('.modal.fade.in .modal-footer .btn-primary').click();")
        time.sleep(10)

        self.assertEqual('rgb(63, 192, 255)', self.browser.execute_script("return $('.col-sm-1 > .school-color').css('background-color')"))
        super().assert_success_message(MSG_SUCCESS_EDIT_SCHOOL_COLOR)

    def test_edit_school_edit_one_field_using_enter(self):
        new_vice_principal = 'Kyoko Kirigiri'
        super().go_to_school_year_page_with_existing_school_year_and_school()
        self.__click_show_button_of_first_school_in_page()
        self.__click_editable_label_of_school_field(self.FIELD_VICE_PRINCIPAL)
        self.__enter_text_in_editable_field(new_vice_principal)
        
        editable_field_element = self.browser.find_element_by_id('editable-field')
        editable_field_element.send_keys(Keys.RETURN)

        self.__assert_one_school_field(self.FIELD_VICE_PRINCIPAL, new_vice_principal)

    def test_edit_school_cancel_one_field_using_esc(self):
        old_address = '123-4567 Test, Setagaya-ku, Tokyo, Japan'
        new_address = 'A test address'
        super().go_to_school_year_page_with_existing_school_year_and_school()
        self.__click_show_button_of_first_school_in_page()
        self.__click_editable_label_of_school_field(self.FIELD_ADDRESS)
        self.__enter_text_in_editable_field(new_address)
        
        editable_field_element = self.browser.find_element_by_id('editable-field')
        editable_field_element.send_keys(Keys.ESCAPE)

        self.__assert_one_school_field(self.FIELD_ADDRESS, old_address)

    def test_edit_school_check_school_year_school_independence(self):
        super().go_to_school_year_page_with_existing_school_year_and_school()
        # Add another school year 
        super().save_new_school_year('2018-04-15', '2019-03-31')
        
        # Click new schoolyear
        element = self.browser.find_element_by_link_text('2018 ~ 2019')
        element.click()
        time.sleep(MODAL_TRANSITION_WAIT_TIME)

        # Add the same school
        school_name = 'School of Hope'
        kanji_name = '希望の高校'
        school_type = (HIGH_SCHOOL, NAME_HIGH_SCHOOL)
        self.__add_school(school_name, kanji_name, school_type)

        # Click the old school year
        time.sleep(5)
        element = self.browser.find_element_by_link_text('2017 ~ 2018')
        element.click()
        time.sleep(MODAL_TRANSITION_WAIT_TIME)

        # Edit the old school year
        self.__edit_one_school_field(self.FIELD_WEBSITE, 'http://google.com')
        
        # Assert that the new school year's data is unchagned even after the old school in the old school year is edited
        element = self.browser.find_element_by_link_text('2018 ~ 2019')
        element.click()
        time.sleep(MODAL_TRANSITION_WAIT_TIME)

        self.__assert_one_school_field(self.FIELD_WEBSITE, 'http://example.com')

    def test_edit_school_with_leading_and_trailing_spaces(self):
        super().go_to_school_year_page_with_existing_school_year_and_school()
        self.__edit_one_school_field(self.FIELD_ENGLISH_HEAD_TEACHER, '   Chisa Yukizome    ')
        self.__assert_one_school_field(self.FIELD_ENGLISH_HEAD_TEACHER, 'Chisa Yukizome')

    