import time, os
import selenium
from lessons.models import *
from paw.constants.tests import *
from paw.constants.models import *
from lessons.constants import *
from datetime import datetime, timedelta
from selenium.webdriver.common.keys import Keys
from home.tests.tests import HomeTestMethods

class DashboardTestCases(HomeTestMethods):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    # Actions
    def __download_lesson_plan_today(self):
        button = self.browser.find_element_by_class_name('btn-primary')
        button.click()
        time.sleep(MODAL_TRANSITION_WAIT_TIME)

    def __download_weekly_lesson_plan(self):
        button = self.browser.find_element_by_class_name('btn-print-week')
        button.click()
        time.sleep(MODAL_TRANSITION_WAIT_TIME)

    def __go_to_lesson_plan(self):
        button = self.browser.find_element_by_class_name('btn-smaller')
        button.click()
        time.sleep(PAGE_LOADING_WAIT_TIME)

    # Assertions
    def __assert_no_classes(self):
        current_date = datetime.now()
        tomorrow = datetime.now() + timedelta(days=1)
        content = self.browser.find_element_by_id('paw-main-content').text
        self.assertIn('Today, %s %s %s'%(current_date.strftime('%B'), current_date.strftime('%e').strip(), current_date.strftime('(%a)')), content)
        self.assertIn('Tomorrow, %s %s %s'%(tomorrow.strftime('%B'), tomorrow.strftime('%e').strip(), tomorrow.strftime('(%a)')), content)
        for i in range(0, 7):
            date = current_date + timedelta(days=i)
            month = int(date.strftime('%m'))
            day = int(date.strftime('%d'))
            self.assertIn('%d/%d'%(month, day), content)

    def __assert_day_existence(self, materials, activities, sections):
        content = self.browser.find_element_by_id('paw-main-content').text
        self.assertIn(materials, content)
        self.assertIn(activities, content)
        for section in sections:
            self.assertIn('%s %s'%(section['section_name'], section['lesson_name']), content)

    def __assert_schedule_week(self):
        content = self.browser.find_element_by_id('paw-main-content').text
        current_date = datetime.now()
        for i in range(0,7):
            scheduled_date = current_date + timedelta(days=i)
            period_type = 'Normal Schedule'
            weekday = scheduled_date.weekday()
            if weekday == 0: # Monday
                period_type = 'Monday Schedule'
            elif weekday == 2: # Wednesday
                period_type = 'Wednesday Schedule'
            month = int(scheduled_date.strftime('%m'))
            day = int(scheduled_date.strftime('%d'))
            self.assertIn('%d/%d\n%s Dolphin Elementary School\n%s\n4-1\n4-2\n4-3'%(month, day, scheduled_date.strftime('%a'), period_type), content)

    # Tests
    # python3 manage.py test home.tests.test_dashboard.DashboardTestCases.test_dashboard_display
    def test_dashboard_display(self):
        super().go_to_dashboard()
        self.__assert_no_classes()

    def test_404(self):
        super().go_to_404_page()
    
    def test_500(self):
        super().go_to_500_page()

    def test_filled_dashboard_today_tomorrow(self):
        super().go_to_dashboard_with_classes_for_today_and_tomorrow()
        self.__assert_day_existence(
            materials='CD, Ohajiki Marbles, Cats', 
            activities='Hello Song; Rainbow Song; Vocabulary Drilling; Keyword Game; Interview Game; Signature Count; Vocabulary Volunteer', 
            sections=[{
                    'section_name': '3-1',
                    'lesson_name': 'Lesson 1, Hour 1'
                }, {
                    'section_name': '3-2',
                    'lesson_name': 'Lesson 1, Hour 1'
                }
            ])
        self.__assert_day_existence(
            materials='CD, Ohajiki Marbles, Cats', 
            activities='Hello Song; Rainbow Song; Vocabulary Drilling; Keyword Game; Interview Game; Signature Count; Vocabulary Volunteer', 
            sections=[{
                    'section_name': '2-A',
                    'lesson_name': 'Lesson 1, Hour 1'
                }, {
                    'section_name': '2-B',
                    'lesson_name': 'Lesson 1, Hour 1'
                }
            ])

    def test_filled_dashboard_week(self):
        super().go_to_dashboard_with_classes_for_the_week()
        self.__assert_schedule_week()

    def test_print_schedule_today(self):
        super().go_to_dashboard_with_classes_for_the_week()
        self.__download_lesson_plan_today()
        super().assert_download_did_not_fail()

    def test_print_schedule_week(self):
        super().go_to_dashboard_with_classes_for_the_week()
        self.__download_weekly_lesson_plan()
        super().assert_download_did_not_fail()

    def test_view_lesson_plan(self):
        super().go_to_dashboard_with_classes_for_the_week()
        self.__go_to_lesson_plan()
        
        content = self.browser.find_element_by_id('paw-main-content').text
        self.assertIn("Dolphin Elementary School, Class 4-1", content)
        self.assertIn("Let's Try 1, Lesson 1, Hour 1", content)

    def test_alt_meeting_work_day(self):
        super().go_to_dashboard_with_alt_meeting_work_day()
        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        content = self.browser.find_element_by_id('paw-main-content').text
        self.assertIn('Today, %s %s %s ALT Meeting'%(today.strftime('%B'), today.strftime('%e').strip(), today.strftime('(%a)')), content)
        self.assertIn('Tomorrow, %s %s %s Work day'%(tomorrow.strftime('%B'), tomorrow.strftime('%e').strip(), tomorrow.strftime('(%a)')), content)
