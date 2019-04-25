import math
import time
import selenium
from schoolyears.models import *
from paw.constants.tests import *
from schoolyears.constants import *
from datetime import datetime, timedelta
from selenium.webdriver.common.keys import Keys
from schoolyears.tests.tests import SchoolYearTestMethods
from selenium.webdriver.common.action_chains import ActionChains

class ScheduleManagingTestCases(SchoolYearTestMethods):

    # Note: Update the colors if the school color has changed!
    BLANK = '#EEE'
    DROPDOWN_1_SOH = {'index': 1, 'color': 'rgb(151, 255, 173)', 'name': 'School of Hope', 'pk':1}
    DROPDOWN_2_TLA = {'index': 2, 'color': 'rgb(240, 143, 144)', 'name': 'Themis Legal Academy', 'pk':2}
    DROPDOWN_3_TBA = {'index': 3, 'color': 'rgb(212, 175, 55)', 'name': 'TBA'}
    DROPDOWN_4_ALT = {'index': 4, 'color': 'rgb(188, 170, 164)', 'name': 'ALT Meeting'}
    DROPDOWN_5_WKD = {'index': 5, 'color': 'rgb(204, 146, 89)', 'name': 'Work day'}

    def setUp(self):
        super().setUp()

    def tearDown(self):
        self.__click_save_calendar_button()
        super().tearDown()

    def __go_to_schedule_page(self):
        super().click_button('btn-edit-schedule')
        time.sleep(PAGE_LOADING_WAIT_TIME)

    def __go_to_schedule_page_with_existing_school_year_and_two_schools(self):
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
            school_colors=GREEN,
            school_type=HIGH_SCHOOL,
            school_year=SchoolYear.objects.first(),
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
        new_school_entry = School(
            school_colors=BLUE,
            school_type=JUNIOR_HIGH_SCHOOL,
            school_year=SchoolYear.objects.first(),
            name='Themis Legal Academy',
            name_kanji='テミス法律学園',
            address='123-4567 Test, Meguro-ku, Tokyo, Japan',
            contact_number='080-1235-8132',
            website='http://themislegalacademy.co.jp',
            principal='Aristotle Means',
            vice_principal='Constance Courte',
            english_head_teacher='Dick Gumshoe'
        )
        new_school_entry.save()
        self.browser.get('%s%s' % (self.live_server_url, '/schoolyears/'))
        time.sleep(PAGE_LOADING_WAIT_TIME)
        self.__go_to_schedule_page()

    def __click_download_button(self):
        element = self.browser.find_element_by_id('btn-download-ics')
        element.click()

    def __select_dropdown_value(self, dropdown_option):
        index = str(dropdown_option['index'])

        dropdown = self.browser.find_element_by_css_selector('.active-school-dropdown select')
        dropdown.click()
        element = self.browser.find_element_by_css_selector('.active-school-dropdown select > option:nth-child('+index+')')
        element.click()
        element = self.browser.find_element_by_css_selector('.active-school-dropdown select')
        element.click()

    def __assert_color_of_element_with_css_selector(self, css_selector, target_color):
        element = self.browser.find_element_by_css_selector(css_selector)
        self.assertEqual(element.value_of_css_property('background-color'), target_color)

    def __assert_color_of_active_dropdown(self, target_color):
        self.__assert_color_of_element_with_css_selector('#edit-school-color', target_color)

    def __assert_color_of_date_range(self, date_array, target_color):
        for date in date_array:
            self.__assert_color_of_date(date, target_color)

    def __assert_color_of_date(self, date, target_color):
        element = self.browser.find_element_by_id(date)
        self.assertEqual(element.get_attribute('style'), target_color)

    def __assert_no_color_date(self, date):
        element = self.browser.find_element_by_id(date)
        self.assertEqual(element.get_attribute('style'), '')

    def __click_date(self, date):
        element = self.browser.find_element_by_id(date)
        element.click()

    def __click_and_drag(self, start_date, end_date):
        source_element = self.browser.find_element_by_id(start_date)
        destination_element = self.browser.find_element_by_id(end_date)
        ActionChains(self.browser).drag_and_drop(source_element, destination_element).perform()

    def __shift_click_dates(self, start_date, end_date):
        self.__click_date(start_date)
        shift_key_down = ActionChains(self.browser).key_down(Keys.SHIFT)
        shift_key_up = ActionChains(self.browser).key_up(Keys.SHIFT)

        shift_key_down.perform()
        self.__click_date(end_date)
        shift_key_up.perform()

    def __construct_date_background_color(self, color_array):
        color_count = len(color_array)
        percentage_current = 0
        percentage_increment = 100/color_count
        percentage_display = round(percentage_current, 4)
        background_string = 'background: rgba(0, 0, 0, 0) linear-gradient('
        for index, item in enumerate(color_array):
            background_string += str(item) + ' '
            background_string += str(percentage_display) + '%, '
            
            percentage_current += percentage_increment
            percentage_display = str(round(percentage_current, 4))
            percentage_display = percentage_display.rstrip('0').rstrip('.') if '.0' in percentage_display else percentage_display

            background_string += str(item) + ' '
            background_string += str(percentage_display) + '%'
            if index != color_count - 1:
                background_string += ', '

        background_string += ') repeat scroll 0% 0%;'
        return background_string

    def __click_save_calendar_button(self):
        save_button = self.browser.find_element_by_id('btn-save')
        save_button.click()
        time.sleep(MODAL_TRANSITION_WAIT_TIME)

    def __click_undo_calendar_button(self):
        undo_button = self.browser.find_element_by_id('btn-undo')
        undo_button.click()

    def __go_back_to_school_years_page(self):
        back_button = self.browser.find_element_by_link_text('Back to school year page')
        back_button.click()

    def test_dropdown_values(self):
        self.__go_to_schedule_page_with_existing_school_year_and_two_schools()

        option_1 = self.browser.find_element_by_css_selector('.active-school-dropdown select > option:nth-child(1)')
        option_2 = self.browser.find_element_by_css_selector('.active-school-dropdown select > option:nth-child(2)')
        option_3 = self.browser.find_element_by_css_selector('.active-school-dropdown select > option:nth-child(3)')
        option_4 = self.browser.find_element_by_css_selector('.active-school-dropdown select > option:nth-child(4)')
        option_5 = self.browser.find_element_by_css_selector('.active-school-dropdown select > option:nth-child(5)')
        
        time.sleep(PAGE_LOADING_WAIT_TIME)
        self.assertEqual(self.DROPDOWN_1_SOH['name'], option_1.text)
        self.assertEqual(self.DROPDOWN_2_TLA['name'], option_2.text)
        self.assertEqual(self.DROPDOWN_3_TBA['name'], option_3.text)
        self.assertEqual(self.DROPDOWN_4_ALT['name'], option_4.text)
        self.assertEqual(self.DROPDOWN_5_WKD['name'], option_5.text)

    def test_dropdown_color(self):
        self.__go_to_schedule_page_with_existing_school_year_and_two_schools()

        time.sleep(PAGE_LOADING_WAIT_TIME)
        self.__assert_color_of_active_dropdown(self.DROPDOWN_1_SOH['color'])
        self.__select_dropdown_value(self.DROPDOWN_2_TLA)

        time.sleep(PAGE_LOADING_WAIT_TIME)
        self.__assert_color_of_active_dropdown(self.DROPDOWN_2_TLA['color'])
        self.__select_dropdown_value(self.DROPDOWN_3_TBA)

        time.sleep(PAGE_LOADING_WAIT_TIME)
        self.__assert_color_of_active_dropdown(self.DROPDOWN_3_TBA['color'])
        self.__select_dropdown_value(self.DROPDOWN_4_ALT)

        time.sleep(PAGE_LOADING_WAIT_TIME)
        self.__assert_color_of_active_dropdown(self.DROPDOWN_4_ALT['color'])
        self.__select_dropdown_value(self.DROPDOWN_5_WKD)

        time.sleep(PAGE_LOADING_WAIT_TIME)
        self.__assert_color_of_active_dropdown(self.DROPDOWN_5_WKD['color'])

    def test_toggle_date(self):
        self.__go_to_schedule_page_with_existing_school_year_and_two_schools()
        date = '2017-04-12'
        self.__click_date(date)
        time.sleep(PAGE_LOADING_WAIT_TIME)
        self.__assert_color_of_date(date, self.__construct_date_background_color([self.DROPDOWN_1_SOH['color']]))
        self.__click_date(date)
        time.sleep(PAGE_LOADING_WAIT_TIME)
        self.__assert_no_color_date(date)

    def test_drag(self):
        self.__go_to_schedule_page_with_existing_school_year_and_two_schools()

        self.__select_dropdown_value(self.DROPDOWN_4_ALT)
        self.__click_and_drag('2017-04-02', '2017-04-23')
        
        self.__select_dropdown_value(self.DROPDOWN_2_TLA)
        self.__click_and_drag('2017-04-03', '2017-04-07')

        alt_background_color = self.__construct_date_background_color([self.DROPDOWN_4_ALT['color']])
        tla_background_color = self.__construct_date_background_color([self.DROPDOWN_2_TLA['color']])

        time.sleep(PAGE_LOADING_WAIT_TIME)
        self.__assert_color_of_date_range(['2017-04-02', '2017-04-09', '2017-04-16', '2017-04-23'], alt_background_color)
        self.__assert_color_of_date_range(['2017-04-03', '2017-04-04', '2017-04-05', '2017-04-06', '2017-04-07'], tla_background_color)

    def test_shift_click(self):
        self.__go_to_schedule_page_with_existing_school_year_and_two_schools()
        self.__select_dropdown_value(self.DROPDOWN_3_TBA)
        start_date = '2017-04-15'
        end_date = '2017-06-03'
        self.__shift_click_dates(start_date, end_date)

        # April
        date_range = []
        assert_april = '2017-04-'
        base_day = 15
        for i in range(16):
            date_range.append(assert_april + str(base_day + i))

        # May
        assert_may = '2017-05-'
        for i in range(31):
            readable_day = i + 1
            if readable_day < 10:
                readable_day = str('0') + str(readable_day)
            date_range.append(assert_may + str(readable_day))

        # June
        date_range.append('2017-06-01')
        date_range.append('2017-06-02')
        date_range.append('2017-06-03')

        time.sleep(PAGE_LOADING_WAIT_TIME)
        self.__assert_color_of_date_range(date_range, self.__construct_date_background_color([self.DROPDOWN_3_TBA['color']]))

    def test_three_events_one_day(self):
        self.__go_to_schedule_page_with_existing_school_year_and_two_schools()
        date = '2017-04-20'
        self.__click_date(date)

        self.__select_dropdown_value(self.DROPDOWN_2_TLA)
        self.__click_date(date)
        
        self.__select_dropdown_value(self.DROPDOWN_3_TBA)
        self.__click_date(date)
        
        time.sleep(PAGE_LOADING_WAIT_TIME)
        target_color = self.__construct_date_background_color([self.DROPDOWN_1_SOH['color'], self.DROPDOWN_2_TLA['color'], self.DROPDOWN_3_TBA['color']])
        self.__assert_color_of_date(date, target_color)

    def inconsistent_test_close_browser_with_unsaved_changes(self):
        self.__go_to_schedule_page_with_existing_school_year_and_two_schools()
        
        date = '2017-04-12'
        self.__click_date(date)
        self.__go_back_to_school_years_page()

        alert = self.browser.switch_to_alert()
        alert.accept()
        time.sleep(PAGE_LOADING_WAIT_TIME)
        super().click_button('btn-edit-schedule')

    def test_undo_last_action(self):
        self.__go_to_schedule_page_with_existing_school_year_and_two_schools()
        self.__select_dropdown_value(self.DROPDOWN_2_TLA)
        start_date = '2017-04-15'
        end_date = '2017-04-20'
        self.__shift_click_dates(start_date, end_date)
        self.__click_undo_calendar_button()

        time.sleep(PAGE_LOADING_WAIT_TIME)
        self.__assert_no_color_date('2017-04-15')
        self.__assert_no_color_date('2017-04-16')
        self.__assert_no_color_date('2017-04-17')
        self.__assert_no_color_date('2017-04-18')
        self.__assert_no_color_date('2017-04-19')
        self.__assert_no_color_date('2017-04-20')

    def test_undo_last_action_ctrl_z(self):
        self.__go_to_schedule_page_with_existing_school_year_and_two_schools()
        self.__select_dropdown_value(self.DROPDOWN_5_WKD)
        start_date = '2017-05-03'
        end_date = '2017-05-24'
        self.__click_and_drag(start_date, end_date)

        control_key_down = ActionChains(self.browser).key_down(Keys.CONTROL).send_keys('z')
        control_key_down.perform()

        time.sleep(PAGE_LOADING_WAIT_TIME)
        self.__assert_no_color_date('2017-05-03')
        self.__assert_no_color_date('2017-05-10')
        self.__assert_no_color_date('2017-05-17')
        self.__assert_no_color_date('2017-05-24')

    def test_save_ctrl_s(self):
        self.__go_to_schedule_page_with_existing_school_year_and_two_schools()
        self.__select_dropdown_value(self.DROPDOWN_5_WKD)
        start_date = '2017-05-03'
        end_date = '2017-05-24'
        self.__click_and_drag(start_date, end_date)

        control_key_down = ActionChains(self.browser).key_down(Keys.CONTROL).send_keys('s')
        control_key_down.perform()

        self.__go_back_to_school_years_page()
        super().click_button('btn-edit-schedule')
        
        time.sleep(PAGE_LOADING_WAIT_TIME)
        self.__assert_color_of_date_range(['2017-05-03', '2017-05-10', '2017-05-17', '2017-05-24'], self.__construct_date_background_color([self.DROPDOWN_5_WKD['color']]))

    def test_check_day_of_first_date(self):
        self.__go_to_schedule_page_with_existing_school_year_and_two_schools()

        month = self.browser.find_element_by_css_selector('.col-sm-6 > .days')
        self.assertIn('<li class="no-day"></li><li class="no-day"></li><li class="no-day"></li><li class="no-day"></li><li class="no-day"></li><li class="no-day"></li><li class="cursor-pointer" id="2017-04-01" data-is-editing="true" data-is-entered="false" data-color-array="[]">1</li>', month.get_attribute('innerHTML'))

    # # Need manual UI testing for this!
    # def test_download_ics_file_import_google_calendar(self):
    #     self.__go_to_schedule_page_with_existing_school_year_and_two_schools()
    #     date = '2017-04-12'
    #     self.__click_date(date)
    #     self.__assert_color_of_date(date, self.__construct_date_background_color([self.DROPDOWN_1_SOH['color']]))
    #     self.__click_download_button()
    #     enter_key_down = ActionChains(self.browser).key_down(Keys.ENTER)
    #     enter_key_down.perform()

    # # Need manual UI testing for this!
    # def test_download_ics_file_import_google_calendar_from_school_year_page(self):
    #     pass

    # # Need manual UI testing for this!
    # def test_instructions(self):
    #     pass

    # Note: Use two different schools on two different days
    def test_add_save_delete_save_verify_days(self):
        self.__go_to_schedule_page_with_existing_school_year_and_two_schools()

        # ADD! School 1: Click + Drag -- 2017-05-02 to 2017-05-30
        self.__select_dropdown_value(self.DROPDOWN_1_SOH)
        self.__click_and_drag('2017-05-02', '2017-05-30')

        # ADD! School 2: Click + Shift -- 2017-05-10 to 2017-05-20
        self.__select_dropdown_value(self.DROPDOWN_2_TLA)
        self.__shift_click_dates('2017-05-10', '2017-05-20')

        # Save and confirm that they are in the database
        self.__click_save_calendar_button()
        schedule_soh = YearlySchedule.objects.filter(school_id=self.DROPDOWN_1_SOH['pk']).values('date')
        schedule_tla = YearlySchedule.objects.filter(school_id=self.DROPDOWN_2_TLA['pk']).values('date')
        expected_dates_soh = ['2017-05-02', '2017-05-09', '2017-05-16', '2017-05-23', '2017-05-30']
        expected_dates_tla = ['2017-05-10', '2017-05-11', '2017-05-12', '2017-05-13', '2017-05-14', '2017-05-15', '2017-05-16', '2017-05-17', '2017-05-18', '2017-05-19', '2017-05-20']
        for index, result_soh in enumerate(schedule_soh):
            self.assertEqual(expected_dates_soh[index], result_soh['date'].strftime('%Y-%m-%d'))
        for index, result_tla in enumerate(schedule_tla):
            self.assertEqual(expected_dates_tla[index], result_tla['date'].strftime('%Y-%m-%d'))

        # Refresh and confirm that they are present in the UI
        self.browser.refresh()
        time.sleep(PAGE_LOADING_WAIT_TIME)
        expected_dates_soh.remove('2017-05-16')
        expected_dates_tla.remove('2017-05-16')
        self.__assert_color_of_date_range(expected_dates_soh, self.__construct_date_background_color([self.DROPDOWN_1_SOH['color']]))
        self.__assert_color_of_date_range(expected_dates_tla, self.__construct_date_background_color([self.DROPDOWN_2_TLA['color']]))
        self.__assert_color_of_date('2017-05-16', self.__construct_date_background_color([self.DROPDOWN_1_SOH['color'], self.DROPDOWN_2_TLA['color']]))

        # Delete a day
        time.sleep(PAGE_LOADING_WAIT_TIME)
        self.__select_dropdown_value(self.DROPDOWN_1_SOH)
        self.__click_date('2017-05-16')
        self.__select_dropdown_value(self.DROPDOWN_2_TLA)
        self.__click_date('2017-05-16')
        self.__click_save_calendar_button()

        # Confirm that the database has the correct information
        schedule_soh = YearlySchedule.objects.filter(school_id=self.DROPDOWN_1_SOH['pk']).values('date')
        schedule_tla = YearlySchedule.objects.filter(school_id=self.DROPDOWN_2_TLA['pk']).values('date')
        for index, result_soh in enumerate(schedule_soh):
            self.assertEqual(expected_dates_soh[index], result_soh['date'].strftime('%Y-%m-%d'))
        for index, result_tla in enumerate(schedule_tla):
            self.assertEqual(expected_dates_tla[index], result_tla['date'].strftime('%Y-%m-%d'))

        # Refresh and confirm that the correct days are present in the UI
        self.browser.refresh()
        time.sleep(PAGE_LOADING_WAIT_TIME)
        self.__assert_color_of_date_range(expected_dates_soh, self.__construct_date_background_color([self.DROPDOWN_1_SOH['color']]))
        self.__assert_color_of_date_range(expected_dates_tla, self.__construct_date_background_color([self.DROPDOWN_2_TLA['color']]))
        self.__assert_no_color_date('2017-05-16')
    