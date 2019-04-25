import time, os
import selenium
from schedules.models import *
from lessons.models import *
from schoolyears.models import SchoolYear, School, YearlySchedule
from paw.constants.tests import *
from paw.constants.models import *
from schedules.constants import *
from datetime import datetime, timedelta
from selenium.webdriver.common.keys import Keys
from schedules.tests.tests import ScheduleTestMethods

class YearLevelManagementTestCases(ScheduleTestMethods):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    # Actions
    def __add_schedule_past_week(self):
        school = School.objects.get(name='Dolphin Elementary School')
        school_year = SchoolYear.objects.get(name='20XY ~ 20XZ')
        current_date = datetime.now()
        for i in range(0,7):
            scheduled_date = current_date - timedelta(days=i)
            if i > 0:
                super().add_yearly_schedule(school_year, school, scheduled_date)

                year_level = SchoolSection.objects.get(school=school, year_level='3')

                weekday = scheduled_date.weekday() # 0 is Monday, 6 is Saturday
                period_type = PERIOD_TYPE_NORMAL
                if weekday == 0:
                    period_type = PERIOD_TYPE_MONDAY
                elif weekday == 2:
                    period_type = PERIOD_TYPE_WEDNESDAY

                school_period = SchoolPeriod.objects.get(period_number=1, school_period_type=SchoolPeriodType.objects.get(school=school, period_type=period_type))

                new_section_period = SectionPeriod(
                    date=scheduled_date,
                    section=Section.objects.get(school_section=year_level, section_name='1'),
                    school_period=school_period,
                    lesson_plan=LessonPlan.objects.get(hour_number=1),
                    lesson_number=1,
                    hour_number=i,
                )
                new_section_period.save()

    def __click_view_year_level_information(self):
        super().click_button('view-year-level-information')
        time.sleep(PAGE_LOADING_WAIT_TIME)

    def __click_junior_high_school_view_year_level_information(self):
        super().choose_option_from_select('select_school', 'Shark Junior High School', is_modal=False)
        self.__click_view_year_level_information()

    def __click_year_level_manage_button(self, year_level):
        button = self.browser.find_element_by_css_selector('tr:nth-child(%d) .btn-secondary'%(year_level+2)) # Header and Special Needs
        button.click()

    def __fill_editable_field(self, new_value):
        editable_field_element = self.browser.find_element_by_id('editable-field')
        editable_field_element.click()
        editable_field_element.clear()
        editable_field_element.send_keys(str(new_value))

        done_button_element = self.browser.find_element_by_id('done-button')
        done_button_element.click()

    def __edit_student_count(self, section_name, new_student_count):
        editable_text = self.browser.find_element_by_css_selector('tr:nth-child(%d) td:nth-child(3) > span'%(section_name+1))
        editable_text.click()
        self.__fill_editable_field(new_student_count)

    def __edit_teacher_name(self, section_name, new_teacher_name):
        editable_text = self.browser.find_element_by_css_selector('tr:nth-child(%d) td:nth-child(2) > span'%(section_name+1))
        editable_text.click()
        self.__fill_editable_field(new_teacher_name)

    def __go_back_from_view_section_page(self, school_name):
        link = self.browser.find_element_by_link_text('Back to Year Levels, Sections, and Books page for %s'%(school_name))
        link.click()

    def __delete_section(self, section_name):
        self.browser.find_element_by_css_selector('tr:nth-child(%d) .btn-tertiary'%(section_name)).click()
        time.sleep(PAGE_LOADING_WAIT_TIME)

    def __add_section(self, teacher_name, student_count, notes, assertion_text):
        super().click_button('add-section-button')
        time.sleep(MODAL_TRANSITION_WAIT_TIME)

        modal = self.browser.find_element_by_css_selector('.modal.fade.in')
        self.assertIn(assertion_text, modal.text)

        super().type_text_in_input('.modal.fade.in #id_teacher_name', teacher_name)
        super().type_text_in_input('.modal.fade.in #id_student_count', student_count)
        super().type_text_in_input('.modal.fade.in #id_notes', notes)
        super().click_modal_save_button()
        time.sleep(PAGE_LOADING_WAIT_TIME)

    def __add_book(self, book):
        button = self.browser.find_element_by_id('assign-book-button')
        button.click()
        time.sleep(MODAL_TRANSITION_WAIT_TIME)

        super().choose_option_from_select('id_book', book, is_modal=True)
        super().click_modal_save_button()

    # Assertions
    def __assert_section_existence(self, section_name, teacher_name, student_count):
        content = self.browser.find_element_by_id('paw-main-content').text
        self.assertIn('%s %s %s'%(section_name, teacher_name, student_count), content)

    def __assert_elementary_school_year_levels(self):
        context = self.browser.find_element_by_id('paw-main-content').text
        self.assertIn('Special Needs 1 30', context)
        self.assertIn('Grade 1 4 120', context)
        self.assertIn('Grade 2 4 120', context)
        self.assertIn('Grade 3 4 120', context)
        self.assertIn('Grade 4 4 120', context)
        self.assertIn('Grade 5 4 120', context)
        self.assertIn('Grade 6 4 120', context)

    def __assert_junior_high_school_year_levels(self):
        context = self.browser.find_element_by_id('paw-main-content').text
        self.assertIn('Special Needs 1 30', context)
        self.assertIn('Grade 1 3 90', context)
        self.assertIn('Grade 2 3 90', context)
        self.assertIn('Grade 3 3 90', context)

    def __assert_total_student_count(self, year_level, total_student_count):
        context = self.browser.find_element_by_css_selector('tr:nth-child(%d) td:nth-child(3)'%(year_level+2)) # Header and Special Needs
        self.assertEqual(str(total_student_count), context.text)

    def __assert_assigned_books(self, books=None):
        content = self.browser.find_element_by_id('paw-main-content').text
        if books is None:
            self.assertIn('There are no assigned books for this year level.\nWould you like to assign a book?', content)
        else:
            for book in books:
                self.assertIn(book, content)

    def __assert_classes_held(self, section_name, classes_held, dates):
        content = self.browser.find_element_by_id('paw-main-content').text
        text = '%s (Classes held: %d)' % (section_name, classes_held)
        self.assertIn(text, content)
        for date in dates:
            self.assertIn(date.strftime('%m/%d'), content)

    # Tests
    # python3 manage.py test schedules.tests.test_manage_year_level.YearLevelManagementTestCases.test_no_school_years_available
    def test_no_school_years_available(self):
        super().go_to_year_level_page()
        super().assert_no_school_years()

    def test_no_schools_available(self):
        super().go_to_year_level_page_with_school_year()
        super().assert_dropdown_enabled('select[name="school-year"]', True)
        super().assert_dropdown_enabled('select[name="school"]', False)

    def test_elementary_school_period_profile(self):
        super().go_to_year_level_with_school()
        self.__click_view_year_level_information()
        self.__assert_elementary_school_year_levels()

    def test_junior_high_school_period_profile(self):
        super().go_to_year_level_with_school()
        self.__click_junior_high_school_view_year_level_information()
        self.__assert_junior_high_school_year_levels()        

    def test_edit_student_count(self):
        super().go_to_year_level_with_school()
        self.__click_view_year_level_information()
        self.__click_year_level_manage_button(year_level=5)
        self.__edit_student_count(section_name=2, new_student_count=25)
        self.__go_back_from_view_section_page('Dolphin Elementary School')
        self.__assert_total_student_count(year_level=5, total_student_count=115)

    def test_delete_elementary_section(self):
        teacher_name = 'Mr. Kageyama'
        super().go_to_year_level_with_school()
        self.__click_view_year_level_information()
        self.__click_year_level_manage_button(year_level=5)
        self.__edit_teacher_name(section_name=3, new_teacher_name=teacher_name)
        self.__delete_section(section_name=2)
        self.__assert_section_existence(section_name='5-1', teacher_name='N/A', student_count='30')
        self.__assert_section_existence(section_name='5-2', teacher_name=teacher_name, student_count='30')
        self.__assert_section_existence(section_name='5-3', teacher_name='N/A', student_count='30')
        self.__go_back_from_view_section_page('Dolphin Elementary School')
        self.__assert_total_student_count(year_level=5, total_student_count=90)

    def test_delete_junior_high_section(self):
        teacher_name = 'Mr. Kageyama'
        super().go_to_year_level_with_school()
        self.__click_junior_high_school_view_year_level_information()
        self.__click_year_level_manage_button(year_level=2)
        self.__edit_teacher_name(section_name=3, new_teacher_name=teacher_name)
        self.__delete_section(section_name=2)
        self.__assert_section_existence(section_name='2-A', teacher_name='N/A', student_count='30')
        self.__assert_section_existence(section_name='2-B', teacher_name=teacher_name, student_count='30')
        self.__go_back_from_view_section_page('Shark Junior High School')
        self.__assert_total_student_count(year_level=2, total_student_count=60)

    def test_add_elementary_school_section(self):
        super().go_to_year_level_with_complete_package()
        self.__click_view_year_level_information()
        self.__click_year_level_manage_button(year_level=3)
        self.__add_section(teacher_name='Ms. Yukizome', student_count=16, notes='Class 77', assertion_text='Grade 3, Section 3-5')
        self.__assert_section_existence(section_name='3-1', teacher_name='Mr. Nogami', student_count='30')
        self.__assert_section_existence(section_name='3-2', teacher_name='N/A', student_count='30')
        self.__assert_section_existence(section_name='3-3', teacher_name='N/A', student_count='30')
        self.__assert_section_existence(section_name='3-4', teacher_name='N/A', student_count='30')
        self.__assert_section_existence(section_name='3-5', teacher_name='Ms. Yukizome', student_count='16')
        self.__go_back_from_view_section_page('Dolphin Elementary School')
        self.__assert_total_student_count(year_level=3, total_student_count=136)

    def test_add_junior_high_school_section(self):
        super().go_to_year_level_with_complete_package()
        self.__click_junior_high_school_view_year_level_information()
        self.__click_year_level_manage_button(year_level=3)
        self.__add_section(teacher_name='Ms. Yukizome', student_count=16, notes='Class 77', assertion_text='Grade 3, Section 3-D')
        self.__assert_section_existence(section_name='3-A', teacher_name='N/A', student_count='30')
        self.__assert_section_existence(section_name='3-B', teacher_name='N/A', student_count='30')
        self.__assert_section_existence(section_name='3-C', teacher_name='N/A', student_count='30')
        self.__assert_section_existence(section_name='3-D', teacher_name='Ms. Yukizome', student_count='16')
        self.__go_back_from_view_section_page('Shark Junior High School')
        self.__assert_total_student_count(year_level=3, total_student_count=106)

    def test_no_book(self):
        super().go_to_year_level_with_complete_package()
        self.__click_view_year_level_information()
        self.__click_year_level_manage_button(year_level=4)
        self.__assert_assigned_books(books=None)

    def test_assign_book(self):
        book = 'Let\'s Try 1'
        super().go_to_year_level_with_complete_package()
        self.__click_view_year_level_information()
        self.__click_year_level_manage_button(year_level=4)
        self.__add_book(book)
        self.__assert_assigned_books(books=[book])

    def test_activities_per_section(self):
        super().go_to_year_level_with_scheduled_class()
        self.__click_view_year_level_information()
        self.__click_year_level_manage_button(year_level=3)
        self.__assert_classes_held(section_name='3-1', classes_held=1, dates=[datetime.now()])

    def test_activities_per_section_view_more(self):
        expected_dates = []
        expected_dates_view_all = []
        current_date = datetime.now()
        for i in range(0,7):
            scheduled_date = current_date - timedelta(days=i)
            expected_dates_view_all.append(scheduled_date)
            if i <= 4:
                expected_dates.append(scheduled_date)

        super().go_to_year_level_with_scheduled_class()
        self.__add_schedule_past_week()
        self.__click_view_year_level_information()
        self.__click_year_level_manage_button(year_level=3)
        self.__assert_classes_held(section_name='3-1', classes_held=7, dates=expected_dates)

        button = self.browser.find_element_by_class_name('btn-view-all')
        button.click()
        time.sleep(PAGE_LOADING_WAIT_TIME)
        
        self.__assert_classes_held(section_name='3-1', classes_held=7, dates=expected_dates_view_all)


