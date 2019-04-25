import time, os
import selenium
from lessons.models import *
from paw.constants.tests import *
from paw.constants.models import *
from lessons.constants import *
from datetime import datetime, timedelta
from selenium.webdriver.common.keys import Keys
from lessons.tests.tests import LessonTestMethods

class FlashcardManagementTestCases(LessonTestMethods):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    # Actions
    def __search_flashcard_target_language(self, search_term):
        super().type_text_in_input('#search-term', search_term)
        button = self.browser.find_element_by_id('btn-search-flashcard')
        button.click()
        time.sleep(PAGE_LOADING_WAIT_TIME)

    def __edit_first_flashcard(self, picture, label, notes, flashcard_type, orientation, is_bordered):
        edit_flashcard_button = self.browser.find_element_by_css_selector('.page-subsubheader-right > .edit-flashcard-button')
        edit_flashcard_button.click()
        time.sleep(MODAL_TRANSITION_WAIT_TIME)
        super().fill_flashcard_modal(picture, label, notes, flashcard_type, orientation, is_bordered)

    def __generate_flashcard(self, picture, label, notes, flashcard_type, orientation, is_bordered):
        super().click_button('generate-flashcard')
        time.sleep(MODAL_TRANSITION_WAIT_TIME)
        super().fill_flashcard_modal(picture, label, notes, flashcard_type, orientation, is_bordered)

    def __generate_target_language(self, target_language, notes, color):
        super().click_button('generate-target-language')
        time.sleep(MODAL_TRANSITION_WAIT_TIME)
        super().fill_target_language_modal(target_language, notes, color)

    # Assertions
    def __assert_flashcard_search_result(self, search_term):
        content = self.browser.find_element_by_class_name('flashcard-table').text
        self.assertIn(search_term, content)

    def __assert_target_language_search_result(self, search_term):
        content = self.browser.find_element_by_class_name('target-language-table').text
        self.assertIn(search_term, content)

    def __assert_no_flashcard_search_result(self):
        self.assertTrue(len(self.browser.find_elements_by_class_name('flashcard-table'))==0)
        content = self.browser.find_element_by_id('paw-main-content').text
        self.assertIn('Your flashcard search yielded no results for the following search term:', content)

    def __assert_no_target_language_search_result(self):
        self.assertTrue(len(self.browser.find_elements_by_class_name('target-language-table'))==0)
        content = self.browser.find_element_by_id('paw-main-content').text
        self.assertIn('Your target language search yielded no results for the following search term:', content)

    # Tests
    # python3 manage.py test lessons.test_manage_flashcards.FlashcardManagementTestCases.test_search_flashcard
    def test_search_flashcard(self):
        search_term = 'Apple'
        self.go_to_flashcard_management_page_with_flashcards_and_target_language()
        self.__search_flashcard_target_language(search_term)
        self.__assert_flashcard_search_result(search_term)
        self.__assert_no_target_language_search_result()

    def test_search_case_insensitivity(self):
        search_term = 'ApPlE'
        self.go_to_flashcard_management_page_with_flashcards_and_target_language()
        self.__search_flashcard_target_language(search_term)
        self.__assert_flashcard_search_result('Apple')

    def test_search_part_of_a_word(self):
        search_term = 'app'
        self.go_to_flashcard_management_page_with_flashcards_and_target_language()
        self.__search_flashcard_target_language(search_term)
        self.__assert_flashcard_search_result('Apple')

    def test_search_two_letters(self):
        search_term = 'ap'
        self.go_to_flashcard_management_page_with_flashcards_and_target_language()
        self.__search_flashcard_target_language(search_term)
        content = self.browser.find_element_by_css_selector('body').text
        self.assertIn('The search term must contain at least three characters.', content)

    def test_search_both_results(self):
        search_term = 'Fruit'
        super().go_to_flashcard_management_page_with_fruit_target_language()
        self.__search_flashcard_target_language(search_term)
        self.__assert_flashcard_search_result('Apple')
        self.__assert_target_language_search_result('I like apples')

    def test_search_target_language(self):
        search_term = 'Feelings'
        self.go_to_flashcard_management_page_with_flashcards_and_target_language()
        self.__search_flashcard_target_language(search_term)
        self.__assert_target_language_search_result('How are you?')
        self.__assert_target_language_search_result('I\'m __.')
        self.__assert_no_flashcard_search_result()

    def test_edit_searched_parent_flashcard(self):
        search_term = 'Apple'
        super().go_to_flashcard_management_page_with_two_books_and_parent_child_flashcards()
        self.__search_flashcard_target_language(search_term)
        self.__assert_flashcard_search_result('Apple')
        self.__assert_flashcard_search_result('LeTr1, Lesson 1')
        self.__assert_flashcard_search_result('LeTr2, Lesson 1')
        self.__edit_first_flashcard(picture=None, label='Apples', notes=None, flashcard_type=None, orientation=None, is_bordered=None)
        self.__assert_flashcard_search_result('Apples')
        self.__assert_flashcard_search_result('LeTr1, Lesson 1')
        self.__assert_flashcard_search_result('LeTr2, Lesson 1')

    def test_delete_searched_parent_flashcard(self):
        search_term = 'Apple'
        super().go_to_flashcard_management_page_with_two_books_and_parent_child_flashcards()
        self.__search_flashcard_target_language(search_term)
        delete_button = self.browser.find_element_by_css_selector('.delete-flashcard-button')
        delete_button.click()
        time.sleep(PAGE_LOADING_WAIT_TIME)
        self.__assert_flashcard_search_result('Apple')
        self.__assert_flashcard_search_result('LeTr2, Lesson 1')

    def test_download_flashcard(self):
        search_term = 'Apple'
        super().go_to_flashcard_management_page_with_two_books_and_parent_child_flashcards()
        self.__search_flashcard_target_language(search_term)
        button = self.browser.find_element_by_class_name('download-flashcard-button')
        button.click()
        super().assert_download_did_not_fail()

    def test_edit_target_language(self):
        search_term = 'How are you'
        super().go_to_flashcard_management_page_with_two_books_and_parent_child_flashcards()
        self.__search_flashcard_target_language(search_term)
        new_target_language = 'How are you doing?'
        super().edit_first_target_language(target_language=new_target_language, notes=None, color=None)
        self.__assert_target_language_search_result(new_target_language)

    def test_delete_target_language(self):
        search_term = 'How are you'
        super().go_to_flashcard_management_page_with_two_books_and_parent_child_flashcards()
        self.__search_flashcard_target_language(search_term)
        super().delete_first_target_language()
        self.__assert_no_target_language_search_result()

    def test_download_target_language(self):
        search_term = 'How are you'
        super().go_to_flashcard_management_page_with_two_books_and_parent_child_flashcards()
        self.__search_flashcard_target_language(search_term)
        button = self.browser.find_element_by_class_name('download-target-language-button')
        button.click()
        super().assert_download_did_not_fail()

    def test_zero_results_all(self):
        search_term = 'asdf'
        self.go_to_flashcard_management_page_with_flashcards_and_target_language()
        self.__search_flashcard_target_language(search_term)
        self.__assert_no_target_language_search_result()
        self.__assert_no_flashcard_search_result()

    def test_generate_target_language(self):
        target_language = 'What fruit do you like?'
        notes = 'Fruits'
        color = NAME_TARGET_LANGUAGE_RED
        self.go_to_flashcard_management_page_with_flashcards_and_target_language()
        self.__generate_target_language(target_language, notes, color)
        super().assert_download_did_not_fail()

    def test_generate_flashcard(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        picture = [os.path.join(BASE_DIR, 'static/media/sample_test_image_3.png')]
        label = 'Carrot'
        notes = 'Vegetables'
        flashcard_type = NAME_PICTURE_ONLY
        orientation = NAME_LANDSCAPE
        is_bordered = True

        self.go_to_flashcard_management_page_with_flashcards_and_target_language()
        self.__generate_flashcard(picture, label, notes, flashcard_type, orientation, is_bordered)
        super().assert_download_did_not_fail()


