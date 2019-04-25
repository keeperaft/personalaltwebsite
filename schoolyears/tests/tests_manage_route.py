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

class RouteManagementTestCases(SchoolYearTestMethods):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    EDIT_ROUTE_INDEX_ROUTE_NAME = 0
    EDIT_ROUTE_INDEX_SOURCE = 1
    EDIT_ROUTE_INDEX_DESTINATION = 2
    EDIT_ROUTE_INDEX_METHOD = 3
    EDIT_ROUTE_INDEX_COST = 4

    METHOD_DROPDOWN_NOT = 0
    METHOD_DROPDOWN_TRA = 1
    METHOD_DROPDOWN_BUS = 2
    METHOD_DROPDOWN_TRB = 3

    def __change_travel_method_of_first_element(self, value_tuple):
        travel_method_dropdown_element = self.browser.find_element_by_css_selector('#school-routes .editable-dropdown')
        travel_method_dropdown_element.click()

        index = str(TRAVEL_METHODS.index(value_tuple) + 1)
        editable_field_element = self.browser.find_element_by_id('editable-field')
        editable_field_element.click()

        element = self.browser.find_element_by_css_selector('#editable-field > option:nth-child('+index+')')
        element.click()
        element = self.browser.find_element_by_css_selector('#editable-field')
        element.click()

        done_button_element = self.browser.find_element_by_id('done-button')
        done_button_element.click()

    def __click_show_button_of_first_school(self):
        show_button = self.browser.find_elements_by_class_name('toggle-visibility')
        if show_button[1].text == 'Show':
            show_button[1].click()

    def __click_round_trip_switch_of_first_school(self):
        self.browser.execute_script("$('table .bootstrap-switch input').first().click();")
        time.sleep(BOOTSTRAP_SWITCH_TRANSITION_WAIT_TIME)

    def __add_new_home_station_of_first_school(self, station_name):
        self.__click_show_button_of_first_school()
        add_home_station_button = self.browser.find_element_by_css_selector('.toggle-visibility-target > .btn-primary')
        add_home_station_button.click()
        self.type_text_in_input('.modal.fade.in #id_name', station_name)
        super().click_modal_save_button()

    def __add_new_alt_route(self, route_name, source, destination, travel_method_tuple, cost, is_round_trip):
        super().click_button('add-route-button')
        self.type_text_in_input('.modal.fade.in #id_route_name', route_name)
        self.type_text_in_input('.modal.fade.in #id_source_name', source)
        self.type_text_in_input('.modal.fade.in #id_destination_name', destination)
        self.type_text_in_input('.modal.fade.in #id_total_cost', cost)

        travel_method_dropdown_element = self.browser.find_element_by_css_selector('.modal.fade.in #id_travel_method')
        travel_method_dropdown_element.click()
        index = str(TRAVEL_METHODS.index(travel_method_tuple) + 1)
        element = self.browser.find_element_by_css_selector('.modal.fade.in #id_travel_method > option:nth-child('+index+')')
        element.click()
        element = self.browser.find_element_by_css_selector('.modal.fade.in #id_travel_method')
        element.click()

        if not is_round_trip:
            self.browser.execute_script("$('.modal.fade.in .bootstrap-switch input').first().click();")
            time.sleep(BOOTSTRAP_SWITCH_TRANSITION_WAIT_TIME)

        super().click_modal_save_button()
        time.sleep(PAGE_LOADING_WAIT_TIME)

    def __add_new_route_of_first_school(self, means_of_travel, start_time, end_time, cost, destination_station):
        self.__click_show_button_of_first_school()
        add_new_route_button = self.browser.find_element_by_css_selector('.toggle-visibility-target > .travel-path > .btn-primary')
        add_new_route_button.click()

        super().type_text_in_input('.modal.fade.in #id_travel_vehicle_name', means_of_travel)
        super().type_text_in_input('.modal.fade.in #id_start_time', start_time)
        super().type_text_in_input('.modal.fade.in #id_end_time', end_time)
        super().type_text_in_input('.modal.fade.in #id_cost', cost)
        super().type_text_in_input('.modal.fade.in #id_name', destination_station)
        super().click_modal_save_button()

    def __edit_route_field_of_first_item(self, field, value):
        editable_label_elements = self.browser.find_elements_by_css_selector('#school-routes .editable-label')
        field_element = editable_label_elements[field]
        field_element.click()

        editable_field_element = self.browser.find_element_by_id('editable-field')
        editable_field_element.click()
        editable_field_element.clear()
        editable_field_element.send_keys(value)

        done_button_element = self.browser.find_element_by_id('done-button')
        done_button_element.click()

    def __add_new_school_year_school_home_station(self):
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
        new_node_entry = Node(
            name='Hachioji Station'
        )
        new_node_entry.save()

    def __go_to_school_year_page_with_existing_school_year_and_school_and_home_station(self):
        self.__add_new_school_year_school_home_station()
        new_source_route = RouteInfo(
            node = Node.objects.first(),
            next_path = None,
            next_route = None
        )
        new_source_route.save()
        new_school_route_entry = SchoolRoute(
            school_year=SchoolYear.objects.first(),
            school=School.objects.first(),
            source_route_info=RouteInfo.objects.first(),
            route_name='Tana ES',
            source_name='Hachioji Station',
            destination_name='Tana Bus Terminal',
            is_round_trip=True,
            total_cost=330,
            is_alt_meeting=False,
            calculated_total_cost=660
        )
        new_school_route_entry.save()
        self.browser.get('%s%s' % (self.live_server_url, '/schoolyears/'))
        time.sleep(PAGE_LOADING_WAIT_TIME)

    def __go_to_school_year_with_existing_school_and_route(self):
        self.__add_new_school_year_school_home_station()
        new_path = Path(
            travel_vehicle_name='JR Chuo Line',
            start_time='7:20',
            end_time='7:24',
            cost=330,
        )
        new_path.save()
        new_source_route = RouteInfo(
            node = Node.objects.first(),
            next_path = Path.objects.first(),
            next_route = None
        )
        new_source_route.save()
        new_school_route_entry = SchoolRoute(
            school_year=SchoolYear.objects.first(),
            school=School.objects.first(),
            source_route_info=RouteInfo.objects.first(),
            route_name='Tana ES',
            source_name='Hachioji Station',
            destination_name='Tana Bus Terminal',
            is_round_trip=True,
            travel_method=TRAVEL_METHOD_ID_TRAIN_BUS,
            total_cost=330,
            is_alt_meeting=False,
            calculated_total_cost=660
        )
        new_school_route_entry.save()
        self.browser.get('%s%s' % (self.live_server_url, '/schoolyears/'))
        time.sleep(PAGE_LOADING_WAIT_TIME)

    def __assert_home_station_existence(self, node_name):
        # Check if it exists in database
        self.assertEqual(Node.objects.all().count(), 1)

        if RouteInfo.objects.all().count() < 1:
            # I'm doing this because Selenium's primitive ass doesn't have something as simple as AssertGreaterThan
            self.assertTrue(False) # Route info does not have any element inside

        if SchoolRoute.objects.all().count() < 1:
            # I'm doing this because Selenium's primitive ass doesn't have something as simple as AssertGreaterThan
            self.assertTrue(False) # School route does not have any element inside

        # Confirm that the newly added element is there
        self.__click_show_button_of_first_school()
        travel_node = self.browser.find_element_by_class_name('travel-node-text')
        self.assertEqual(travel_node.text, node_name)

        super().assert_success_message(MSG_SUCCESS_ADD_HOME_STATION)

    def __assert_existence_of_first_route_in_first_school(self, home_station, 
        means_of_travel, start_time, end_time, cost, destination_station):
        # Check if it exists in database
        self.assertTrue(Node.objects.filter(name=home_station).exists())
        self.assertEqual(SchoolRoute.objects.all().count(), 1)
        self.assertTrue(Path.objects.filter(
            travel_vehicle_name=means_of_travel,
            start_time=start_time,
            end_time=end_time,
            cost=cost
        ).exists())

        if RouteInfo.objects.all().count() < 1:
            # I'm doing this because Selenium's primitive ass doesn't have something as simple as AssertGreaterThan
            self.assertTrue(False) # Route info does not have any element inside

        # Confirm that the newly added element is there
        self.__click_show_button_of_first_school()
        travel_nodes = self.browser.find_elements_by_class_name('travel-node-text')
        self.assertEqual(travel_nodes[0].text, home_station)
        self.assertEqual(travel_nodes[1].text, destination_station)

        travel_mode = self.browser.find_element_by_css_selector('.editable-route > .travel-mode')
        travel_time = self.browser.find_element_by_css_selector('.editable-route > .travel-time')
        travel_cost = self.browser.find_element_by_css_selector('.editable-route > .travel-cost')

        self.assertEqual(travel_mode.text, means_of_travel)
        self.assertEqual(travel_time.text, '0'+str(start_time)+' ~ 0'+str(end_time))
        self.assertEqual(travel_cost.text, '¥ '+str(cost))

        super().assert_success_message(MSG_SUCCESS_ADD_ROUTE)

    def __assert_route_field_of_first_item(self, route_name, source, destination, method, is_round_trip, cost):
        editable_label_elements = self.browser.find_elements_by_css_selector('#school-routes .editable-label')
        on_switch_list = self.browser.find_elements_by_css_selector('table .bootstrap-switch-on')

        self.assertEqual(editable_label_elements[self.EDIT_ROUTE_INDEX_ROUTE_NAME].text, route_name)
        self.assertEqual(editable_label_elements[self.EDIT_ROUTE_INDEX_SOURCE].text, source)
        self.assertEqual(editable_label_elements[self.EDIT_ROUTE_INDEX_DESTINATION].text, destination)
        self.assertEqual(editable_label_elements[self.EDIT_ROUTE_INDEX_METHOD].text, method)
        self.assertEqual(editable_label_elements[self.EDIT_ROUTE_INDEX_COST].text, str(cost))
        self.assertEqual(len(on_switch_list) != 0, is_round_trip)

    def __assert_calculated_cost(self, calculated_cost):
        total_cost_element = self.browser.find_element_by_id('calculated-total-cost-1')
        self.assertEqual(total_cost_element.text, str(calculated_cost))

    def test_add_home_station(self):
        station_name = 'Hachioji Station'
        super().go_to_school_year_page_with_existing_school_year_and_school()
        self.__add_new_home_station_of_first_school(station_name)
        time.sleep(PAGE_LOADING_WAIT_TIME)
        self.__assert_home_station_existence(station_name)

    def test_add_home_station_spaces(self):
        station_name = '     Hashimoto Station     '
        station_name_trimmed = 'Hashimoto Station'
        super().go_to_school_year_page_with_existing_school_year_and_school()
        self.__add_new_home_station_of_first_school(station_name)
        time.sleep(PAGE_LOADING_WAIT_TIME)
        self.__assert_home_station_existence(station_name_trimmed)

    def test_add_home_station_missing_fields(self):
        station_name = '     '
        super().go_to_school_year_page_with_existing_school_year_and_school()
        self.__add_new_home_station_of_first_school(station_name)
        time.sleep(PAGE_LOADING_WAIT_TIME)
        super().assert_modal_error_message(MSG_ERR_ADD_HOME_STATION)

    def test_add_route(self):
        means_of_travel = 'JR Chuo Line'
        start_time = '7:20'
        end_time = '7:24'
        cost = '150'
        destination_name = 'Hashimoto Station'
        self.__go_to_school_year_page_with_existing_school_year_and_school_and_home_station()
        self.__add_new_route_of_first_school(means_of_travel, start_time, end_time, cost, destination_name)
        time.sleep(PAGE_LOADING_WAIT_TIME)
        self.__assert_existence_of_first_route_in_first_school('Hachioji Station', means_of_travel, start_time, end_time, cost, destination_name)

    def test_add_route_missing_fields(self):
        means_of_travel = '   '
        start_time = '   '
        end_time = '    '
        cost = '0'
        destination_name = '    '
        self.__go_to_school_year_page_with_existing_school_year_and_school_and_home_station()
        self.__add_new_route_of_first_school(means_of_travel, start_time, end_time, cost, destination_name)
        time.sleep(PAGE_LOADING_WAIT_TIME)
        super().assert_modal_error_message(MSG_ERR_ADD_ROUTE)

    def test_add_route_incorrect_time(self):
        means_of_travel = 'JR Chuo Line'
        start_time = '7.20'
        end_time = '7.24'
        cost = '100'
        destination_name = 'Hashimoto Station'
        self.__go_to_school_year_page_with_existing_school_year_and_school_and_home_station()
        self.__add_new_route_of_first_school(means_of_travel, start_time, end_time, cost, destination_name)
        time.sleep(PAGE_LOADING_WAIT_TIME)
        super().assert_modal_error_message(MSG_ERR_ADD_ROUTE)

    def test_add_route_incorrect_cost(self):
        means_of_travel = 'JR Chuo Line'
        start_time = '7:20'
        end_time = '7:24'
        cost = '-10'
        destination_name = 'Hashimoto Station'
        self.__go_to_school_year_page_with_existing_school_year_and_school_and_home_station()
        self.__add_new_route_of_first_school(means_of_travel, start_time, end_time, cost, destination_name)
        time.sleep(PAGE_LOADING_WAIT_TIME)
        super().assert_modal_error_message(MSG_ERR_ADD_ROUTE_COST)

    def test_add_route_zero_cost(self):
        means_of_travel = 'JR Chuo Line'
        start_time = '7:20'
        end_time = '7:24'
        cost = '0'
        destination_name = 'Hashimoto Station'
        self.__go_to_school_year_page_with_existing_school_year_and_school_and_home_station()
        self.__add_new_route_of_first_school(means_of_travel, start_time, end_time, cost, destination_name)
        time.sleep(PAGE_LOADING_WAIT_TIME)
        self.__assert_existence_of_first_route_in_first_school('Hachioji Station', means_of_travel, start_time, end_time, cost, destination_name)

    def test_assert_route_correct_values(self):
        self.__go_to_school_year_with_existing_school_and_route()
        time.sleep(PAGE_LOADING_WAIT_TIME)
        self.__assert_route_field_of_first_item('Tana ES', 'Hachioji Station', 'Tana Bus Terminal', TRAVEL_METHOD_NAME_TRAIN_BUS, True, '330')

    def test_edit_school_route_summary(self):
        new_route_name = 'Yumenooka ES'
        new_source = 'Toyoda Station'
        new_destination = 'Harataima Station'
        new_cost = '200'
        self.__go_to_school_year_with_existing_school_and_route()
        self.__edit_route_field_of_first_item(self.EDIT_ROUTE_INDEX_ROUTE_NAME, new_route_name)
        self.__edit_route_field_of_first_item(self.EDIT_ROUTE_INDEX_SOURCE, new_source)
        self.__edit_route_field_of_first_item(self.EDIT_ROUTE_INDEX_DESTINATION, new_destination)
        self.__edit_route_field_of_first_item(self.EDIT_ROUTE_INDEX_COST, new_cost)
        self.__change_travel_method_of_first_element((TRAVEL_METHOD_ID_TRAIN, TRAVEL_METHOD_NAME_TRAIN))
        self.__click_round_trip_switch_of_first_school()
        time.sleep(PAGE_LOADING_WAIT_TIME)
        self.__assert_route_field_of_first_item(new_route_name, new_source, new_destination, TRAVEL_METHOD_NAME_TRAIN, False, new_cost)

    def test_add_alt_route(self):
        route_name = 'To ALT Meeting'
        source = 'Tana Bus Terminal'
        destination = 'Fuchinobe Station'
        travel_method_tuple = (TRAVEL_METHOD_ID_BUS, TRAVEL_METHOD_NAME_BUS)
        cost = '320'
        is_round_trip = False
        self.__go_to_school_year_with_existing_school_and_route()
        SchoolRoute.objects.all().delete()
        self.__add_new_alt_route(route_name, source, destination, travel_method_tuple, cost, is_round_trip)
        time.sleep(PAGE_LOADING_WAIT_TIME)
        self.__assert_route_field_of_first_item(route_name, source, destination, TRAVEL_METHOD_NAME_BUS, is_round_trip, cost)

    def test_add_alt_route_incorrect_cost(self):
        route_name = 'To ALT Meeting'
        source = 'Tana Bus Terminal'
        destination = 'Fuchinobe Station'
        travel_method_tuple = (TRAVEL_METHOD_ID_BUS, TRAVEL_METHOD_NAME_BUS)
        cost = '-320'
        is_round_trip = False
        self.__go_to_school_year_with_existing_school_and_route()
        self.__add_new_alt_route(route_name, source, destination, travel_method_tuple, cost, is_round_trip)
        time.sleep(PAGE_LOADING_WAIT_TIME)
        super().assert_modal_error_message(MSG_ERR_ADD_ROUTE_COST)

    def test_add_alt_route_spaces(self):
        route_name = '    '
        source = '        '
        destination = ' '
        travel_method_tuple = (TRAVEL_METHOD_ID_BUS, TRAVEL_METHOD_NAME_BUS)
        cost = '320'
        is_round_trip = False
        self.__go_to_school_year_with_existing_school_and_route()
        self.__add_new_alt_route(route_name, source, destination, travel_method_tuple, cost, is_round_trip)
        time.sleep(PAGE_LOADING_WAIT_TIME)
        super().assert_modal_error_message(MSG_ERR_ADD_ROUTE)

    def inconsistent_test_calculated_cost_change_round_trip(self):
        self.__go_to_school_year_with_existing_school_and_route()
        time.sleep(PAGE_LOADING_WAIT_TIME)
        self.__assert_calculated_cost('660')
        self.__click_round_trip_switch_of_first_school()
        time.sleep(PAGE_LOADING_WAIT_TIME)
        self.__assert_calculated_cost('330')

    def inconsistent_test_calculated_cost_change_total_cost(self):
        self.__go_to_school_year_with_existing_school_and_route()
        self.__edit_route_field_of_first_item(self.EDIT_ROUTE_INDEX_COST, '200')
        time.sleep(PAGE_LOADING_WAIT_TIME)
        self.__assert_calculated_cost('400')
        