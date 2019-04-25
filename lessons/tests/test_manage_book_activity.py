import time, os
import selenium
from lessons.models import *
from paw.constants.tests import *
from paw.constants.models import *
from lessons.constants import *
from datetime import datetime, timedelta
from selenium.webdriver.common.keys import Keys
from lessons.tests.tests import LessonTestMethods

class BookActivityManagementTestCases(LessonTestMethods):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def __type_book_with_name(self, name, course_code):
        super().type_text_in_input('.modal.fade.in #id_course_name', name)
        super().type_text_in_input('.modal.fade.in #id_course_code', course_code)
        super().click_modal_save_button()
        time.sleep(PAGE_LOADING_WAIT_TIME)

    def __type_lesson_with_name(self, name):
        super().type_text_in_input('.modal.fade.in #id_title', name)
        super().click_modal_save_button()
        time.sleep(PAGE_LOADING_WAIT_TIME)

    def __add_book_from_sidebar(self, name, course_code):
        self.browser.find_element_by_link_text('+ Add New Book').click()
        time.sleep(MODAL_TRANSITION_WAIT_TIME)
        self.__type_book_with_name(name, course_code)

    def __add_book_from_content(self, name, course_code):
        self.browser.find_element_by_link_text('add a new book?').click()
        time.sleep(MODAL_TRANSITION_WAIT_TIME)
        self.__type_book_with_name(name, course_code)

    def __edit_book_with_new_name(self, name, course_code):
        super().click_button('edit-course')
        time.sleep(MODAL_TRANSITION_WAIT_TIME)
        self.__type_book_with_name(name, course_code)

    def __add_lesson_with_name(self, name, new_lesson_number=None):
        super().click_button('add-lesson')
        time.sleep(MODAL_TRANSITION_WAIT_TIME)
        if new_lesson_number is not None:
            self.__assert_modal_lesson_number(new_lesson_number)
        self.__type_lesson_with_name(name)

    def __edit_lesson_name(self, old_name, new_name):
        lesson_elements = self.browser.find_elements_by_class_name('editable-label')
        old_lesson = None
        for element in lesson_elements:
            if element.text ==  old_name:
                old_lesson = element
                break
        if old_lesson is None:
            raise Exception('The lesson, "%s", does not exist in the page.'%(old_name))
        old_lesson.click()

        editable_field_element = self.browser.find_element_by_id('editable-field')
        editable_field_element.click()
        editable_field_element.clear()
        editable_field_element.send_keys(new_name)

        done_button_element = self.browser.find_element_by_id('done-button')
        done_button_element.click()
        time.sleep(PAGE_LOADING_WAIT_TIME)

    def __edit_lesson_name_from_lessons_page(self, new_name):
        super().click_button('edit-lesson')
        super().type_text_in_input('.modal.fade.in #id_title', new_name)
        super().click_modal_save_button()
        time.sleep(PAGE_LOADING_WAIT_TIME)

    def __add_activity(self, name, description, option, materials):
        super().type_text_in_input('.modal.fade.in #id_activity_name', name)
        super().type_text_in_input('.modal.fade.in #id_description', description)
        super().choose_option_from_select('id_activity_skill_type', option)
        super().type_text_in_input('.modal.fade.in #id_materials', materials)
        super().click_modal_save_button()
        time.sleep(PAGE_LOADING_WAIT_TIME)

    def __add_book_activity(self, name, description, option, materials):
        super().click_button('add-book-activity')
        time.sleep(MODAL_TRANSITION_WAIT_TIME)
        self.__add_activity(name, description, option, materials)

    def __add_free_activity(self, name, description, option, materials):
        super().click_button('add-free-activity')
        time.sleep(MODAL_TRANSITION_WAIT_TIME)
        self.__add_activity(name, description, option, materials)

    def __add_handout(self, notes):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_directory = [os.path.join(BASE_DIR, 'static/media/sample-file.txt')]

        self.browser.find_element_by_link_text('Add Handouts').click()
        time.sleep(PAGE_LOADING_WAIT_TIME)

        super().click_button('add-file')
        time.sleep(MODAL_TRANSITION_WAIT_TIME)

        super().type_text_in_input('.modal.fade.in #id_notes', notes)
        self.browser.find_element_by_id('id_activity_file').send_keys(file_directory)
        super().click_modal_save_button()
        time.sleep(PAGE_LOADING_WAIT_TIME)

    def __edit_first_book_activity(self, new_name, new_description, new_option, new_materials):
        edit_button = self.browser.find_element_by_css_selector('td.page-subsubheader-right > .btn-primary')
        edit_button.click()
        time.sleep(MODAL_TRANSITION_WAIT_TIME)
        self.__add_activity(new_name, new_description, new_option, new_materials)

    def __edit_first_book_activity_from_view_activity_page(self, new_name, new_description, new_option, new_materials):
        self.browser.find_element_by_link_text('Add Handouts').click()
        time.sleep(PAGE_LOADING_WAIT_TIME)

        edit_button = self.browser.find_element_by_css_selector('.page-header-right > .btn-primary')
        edit_button.click()
        time.sleep(MODAL_TRANSITION_WAIT_TIME)
        self.__add_activity(new_name, new_description, new_option, new_materials)

    def __add_flashcard(self, picture, label, notes, flashcard_type, orientation, is_bordered):
        self.browser.execute_script("$('button:contains(\"Add Flashcard\")').click()")
        time.sleep(MODAL_TRANSITION_WAIT_TIME)
        super().fill_flashcard_modal(picture, label, notes, flashcard_type, orientation, is_bordered)
        
    def __edit_first_flashcard(self, picture, label, notes, flashcard_type, orientation, is_bordered):
        edit_flashcard_button = self.browser.find_element_by_css_selector('.page-subsubheader-right > .edit-flashcard-button')
        edit_flashcard_button.click()
        time.sleep(MODAL_TRANSITION_WAIT_TIME)
        super().fill_flashcard_modal(None, label, notes, flashcard_type, orientation, is_bordered)

    def __add_target_language(self, target_language, notes, color):
        self.browser.execute_script("$('button:contains(\"Add Target Language\")').click()")
        time.sleep(MODAL_TRANSITION_WAIT_TIME)
        super().fill_target_language_modal(target_language, notes, color)

    def __delete_first_flashcard(self):
        delete_button = self.browser.find_element_by_css_selector('.delete-flashcard-button')
        delete_button.click()
        time.sleep(PAGE_LOADING_WAIT_TIME)

    def __add_existing_flashcard(self, flashcard_name):
        super().click_button('add-existing-flashcard')
        time.sleep(MODAL_TRANSITION_WAIT_TIME)
        super().choose_option_from_select('flashcard_id', flashcard_name)
        super().click_modal_save_button()
        time.sleep(PAGE_LOADING_WAIT_TIME)

    # Assertions
    def __assert_book_existence(self, name, course_code):
        self.assertTrue(Course.objects.filter(course_name=name, course_code=course_code).exists())
        sidebar = self.browser.find_element_by_id('paw-sidebar')
        self.assertIn(name, sidebar.text)        

    def __assert_lesson_existence(self, name, lesson_number):
        self.assertTrue(Lesson.objects.filter(title=name, lesson_number=lesson_number).exists())
        content = self.browser.find_element_by_id('paw-main-content')
        self.assertIn(name, content.text) 

    def __assert_modal_lesson_number(self, new_lesson_number):
        modal = self.browser.find_element_by_css_selector('.modal.fade.in #form-modal-title')
        self.assertEqual('Add Lesson %d'%(new_lesson_number), modal.text)

    def __assert_activity_existence(self, name, description, materials, source_type, skill_type):
        self.assertTrue(Activity.objects.filter(activity_source_type=source_type, activity_skill_type=skill_type, activity_name=name, description=description, materials=materials).exists())

        content = self.browser.find_element_by_id('paw-main-content')
        content_text = content.text
        self.assertIn(name, content_text) 
        self.assertIn(materials, content_text) 

    def __assert_activity_inexistence(self, name, description, materials, source_type, skill_type):
        self.assertFalse(Activity.objects.filter(activity_source_type=source_type, activity_skill_type=skill_type, activity_name=name, description=description, materials=materials).exists())

    def __assert_handout_existence(self, notes):
        self.assertTrue(ActivityFile.objects.filter(notes=notes).exists())
        content = self.browser.find_element_by_id('paw-main-content')
        self.assertIn(notes, content.text) 
        button = self.browser.find_element_by_css_selector('.page-subsubheader-right > a > .btn-tertiary')
        button.click()
        time.sleep(PAGE_LOADING_WAIT_TIME)

    def __assert_flashcard_existence(self, label, notes, name_flashcard_type, name_orientation, is_bordered, lesson=None):
        self.assertTrue(Flashcard.objects.filter(label=label, notes=notes).exists())
        if lesson is not None:
            flashcard = Flashcard.objects.get(label=label, notes=notes)
            self.assertTrue(FlashcardLesson.objects.filter(flashcard=flashcard, lesson=lesson))
        content = self.browser.find_element_by_id('paw-main-content').text
        self.assertIn(label, content)
        self.assertIn(notes, content)
        self.assertIn(name_flashcard_type, content)
        self.assertIn(name_orientation, content)

    def __assert_target_language_existence(self, target_language, notes):
        self.assertTrue(TargetLanguage.objects.filter(target_language=target_language, notes=notes).exists())
        content = self.browser.find_element_by_id('paw-main-content').text
        self.assertIn(target_language, content)
        self.assertIn(notes, content)

    def __assert_flashcard_inexistence(self, label, notes, lesson=None):
        self.assertFalse(Flashcard.objects.filter(label=label, notes=notes).exists())
        content = self.browser.find_element_by_id('paw-main-content').text
        self.assertNotIn(label, content)
        self.assertNotIn(notes, content)

    def __assert_target_language_inexistence(self, target_language):
        self.assertFalse(TargetLanguage.objects.filter(target_language=target_language).exists())
        content = self.browser.find_element_by_id('paw-main-content').text
        self.assertNotIn(target_language, content)

    def __assert_flashcard_lesson_existence(self, flashcard, lesson):
        self.assertTrue(FlashcardLesson.objects.filter(flashcard=flashcard, lesson=lesson).exists())

    def __assert_flashcard_lesson_inexistence(self, flashcard, lesson):
        self.assertFalse(FlashcardLesson.objects.filter(flashcard=flashcard, lesson=lesson).exists())

    # python3 manage.py test lessons.test_manage_book_activity.BookActivityManagementTestCases.test_add_book
    def test_add_book(self):
        name = 'Data Structures 2'
        code = 'DaStr2'
        super().go_to_materials_page()
        self.__add_book_from_sidebar(name, code)
        self.__assert_book_existence(name, code)

    def test_add_multiple_books(self):
        name_book_1 = 'Data Structures 2'
        code_book_1 = 'DaStr2'
        name_book_2 = 'Code Complete'
        code_book_2 = 'CoCo'
        super().go_to_materials_page()
        self.__add_book_from_content(name_book_1, code_book_1)
        self.__add_book_from_sidebar(name_book_2, code_book_2)
        self.__assert_book_existence(name_book_1, code_book_1)
        self.__assert_book_existence(name_book_2, code_book_2)

    def test_edit_book_name_and_code(self):
        new_book = 'Code Complete'
        new_code = 'CoCo'
        super().go_to_materials_page_with_existing_book()
        self.__edit_book_with_new_name(new_book, new_code)
        self.__assert_book_existence(new_book, new_code)

    def test_add_lesson(self):
        name = 'Hello, world!'
        super().go_to_materials_page_with_existing_book()
        self.__add_lesson_with_name(name)
        self.__assert_lesson_existence(name=name, lesson_number=1)

    def test_add_multiple_lessons(self):
        name_lesson_1 = 'Hello, world!'
        name_lesson_2 = 'How are you?'
        super().go_to_materials_page_with_existing_book()
        self.__add_lesson_with_name(name_lesson_1, 1)
        self.__add_lesson_with_name(name_lesson_2, 2)
        self.__assert_lesson_existence(name_lesson_1, 1)
        self.__assert_lesson_existence(name_lesson_2, 2)
        
    def test_edit_lesson(self):
        old_name = 'Hello, world!'
        new_name = 'Introduction to Quantum Mechanics'
        super().go_to_materials_page_with_existing_book_and_lesson()
        self.__edit_lesson_name(old_name, new_name)
        self.__assert_lesson_existence(new_name, 1)

    def test_edit_lesson_from_course(self):
        old_name = 'Hello, world!'
        new_name = 'Search Algorithms'
        super().go_to_lessons_page_with_existing_book_and_lesson()
        self.__edit_lesson_name_from_lessons_page(new_name)
        self.__assert_lesson_existence(new_name, 1)

    def test_new_book_activity(self):
        name = 'Problem Solving 1, p.23'
        description = 'Have the students solve the problems in the specified page. The answers are: 1, 5, 19, 30'
        option = NAME_VOCABULARY
        materials = 'Pencils, Erasers'
        super().go_to_lessons_page_with_existing_book_and_lesson()
        self.__add_book_activity(name, description, option, materials)
        self.__assert_activity_existence(name, description, materials, BOOK_BOUND, VOCABULARY)

    def test_new_free_activity(self):
        name = 'Let\'s Listen 1, p.23'
        description = 'The answers are: A, B, A, D'
        option = NAME_CONVERSATION
        materials = 'PC, Ohajiki Marbles'
        super().go_to_lessons_page_with_existing_book_and_lesson()
        self.__add_free_activity(name, description, option, materials)
        self.__assert_activity_existence(name, description, materials, BOOK_FREE, CONVERSATION)

    def test_add_handout_to_book_activity(self):
        notes = 'A sample text file.'
        super().go_to_lessons_page_with_existing_book_lesson_and_activities()
        self.__add_handout(notes)
        self.__assert_handout_existence(notes)

    def test_edit_activity(self):
        new_name = 'Problem Solving 2, p.25'
        new_description = 'Have the students solve the problems in the specified page. The answers are: 1, 5, 19, 30'
        new_option = NAME_LISTENING
        new_materials = 'Calculators'
        super().go_to_lessons_page_with_existing_book_lesson_and_activities()
        self.__edit_first_book_activity(new_name, new_description, new_option, new_materials)
        self.__assert_activity_existence(new_name, new_description, new_materials, BOOK_BOUND, LISTENING)

        old_name = 'Activity, p.23'
        old_description = 'Have the kids walk around the classroom, asking their peers what their favorite food is.'
        old_materials = 'Pencil'
        self.__assert_activity_inexistence(old_name, old_description, old_materials, BOOK_BOUND, CONVERSATION)

    def test_edit_activity_from_view_activity(self):
        new_name = 'Problem Solving 2, p.25'
        new_description = 'Have the students solve the problems in the specified page. The answers are: 1, 5, 19, 30'
        new_option = NAME_LISTENING
        new_materials = 'Calculators'
        super().go_to_lessons_page_with_existing_book_lesson_and_activities()
        self.__edit_first_book_activity_from_view_activity_page(new_name, new_description, new_option, new_materials)
        self.__assert_activity_existence(new_name, new_description, new_materials, BOOK_BOUND, LISTENING)

        old_name = 'Activity, p.23'
        old_description = 'Have the kids walk around the classroom, asking their peers what their favorite food is.'
        old_materials = 'Pencil'
        self.__assert_activity_inexistence(old_name, old_description, old_materials, BOOK_BOUND, CONVERSATION)

    def test_add_flashcard(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        picture_1 = [os.path.join(BASE_DIR, 'static/media/sample_test_image_1.png')]
        label_1 = 'Soccer'
        notes_1 = 'Sports'
        flashcard_type_1 = NAME_PICTURE_LABEL
        orientation_1 = NAME_PORTRAIT
        is_bordered_1 = True

        picture_2 = [os.path.join(BASE_DIR, 'static/media/sample_test_image_2.png')]
        label_2 = 'Apple'
        notes_2 = 'Fruits'
        flashcard_type_2 = NAME_PICTURE_ONLY
        orientation_2 = NAME_LANDSCAPE
        is_bordered_2 = False

        super().go_to_lessons_page_with_existing_book_lesson_and_activities()
        self.__add_flashcard(picture_1, label_1, notes_1, flashcard_type_1, orientation_1, is_bordered_1)
        self.__add_flashcard(picture_2, label_2, notes_2, flashcard_type_2, orientation_2, is_bordered_2)

        # The reason that that is in text is because localization is preventing that from being used in the assertions. 
        self.__assert_flashcard_existence(label_1, notes_1, 'Flashcard with picture and label', 'Portrait', is_bordered_1)
        self.__assert_flashcard_existence(label_2, notes_2, 'Flashcard with picture only', 'Landscape', is_bordered_2)

    def test_edit_flashcard(self):
        super().go_to_lessons_page_with_existing_book_lesson_activities_and_flashcards()

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        picture = [os.path.join(BASE_DIR, 'static/media/sample_test_image_3.png')]
        label = 'Carrot'
        notes = 'Vegetables'
        flashcard_type = NAME_PICTURE_ONLY
        orientation = NAME_LANDSCAPE
        is_bordered = True

        self.__edit_first_flashcard(picture, label, notes, flashcard_type, orientation, is_bordered)
        self.__assert_flashcard_existence(label, notes, 'Flashcard with picture only', 'Landscape', is_bordered)

    def test_add_target_language(self):
        target_language_1 = 'How are you?'
        notes_1 = 'Feelings'
        color_1 = NAME_TARGET_LANGUAGE_RED

        target_language_2 = 'I\'m __.'
        notes_2 = 'Feelings'
        color_2 = NAME_TARGET_LANGUAGE_BLUE
        super().go_to_lessons_page_with_existing_book_lesson_activities_and_flashcards()
        self.__add_target_language(target_language_1, notes_1, color_1)
        self.__add_target_language(target_language_2, notes_2, color_2)
        self.__assert_target_language_existence(target_language_1, notes_1)
        self.__assert_target_language_existence(target_language_2, notes_2)

    def test_edit_target_language(self):
        target_language = 'How are you feeling?'
        notes = 'Feelings 2'
        color = NAME_TARGET_LANGUAGE_RED
        super().go_to_lessons_page_with_existing_book_lesson_activities_flashcards_and_target_languages()
        super().edit_first_target_language(target_language, notes, color)
        self.__assert_target_language_existence(target_language, notes)

    def test_delete_flashcard(self):
        label = 'Apple'
        notes = 'Fruits'
        super().go_to_lessons_page_with_existing_book_lesson_activities_and_flashcards()
        self.__delete_first_flashcard()
        self.__assert_flashcard_inexistence(label, notes)

    def test_delete_target_language(self):
        target_language = 'How are you?'
        notes = 'Feelings'
        super().go_to_lessons_page_with_existing_book_lesson_activities_flashcards_and_target_languages()
        super().delete_first_target_language()
        self.__assert_target_language_inexistence(target_language)

    def test_add_existing_flashcard(self):
        label = 'Soccer'
        notes = 'Sports'
        is_bordered = True
        lesson = super().go_to_lessons_page_with_two_books_lessons_and_flashcards()
        self.__add_existing_flashcard('%s (%s; LeTr1, Lesson 1)'%(label, notes))
        self.__assert_flashcard_existence(label, notes, 'Flashcard with picture and label', 'Portrait', is_bordered, lesson)

        flashcard = Flashcard.objects.get(label=label, notes=notes)
        self.__assert_flashcard_lesson_existence(flashcard, lesson)

    def test_delete_child_flashcard(self):
        label = 'Soccer'
        notes = 'Sports'
        lesson = self.go_to_lessons_page_with_two_books_lessons_and_existing_flashcards()
        flashcard = Flashcard.objects.get(label=label, notes=notes)
        old_lesson = Lesson.objects.get(title='Hello, world!')
        self.__delete_first_flashcard()
        self.__assert_flashcard_lesson_inexistence(flashcard, lesson)
        self.__assert_flashcard_lesson_existence(flashcard, old_lesson)

    def test_delete_parent_flashcard(self):
        label = 'Apple'
        notes = 'Fruits'
        new_lesson = self.go_to_lessons_page_of_first_book_with_two_books()
        old_lesson = Lesson.objects.get(title='Hello, world!')
        flashcard = Flashcard.objects.get(label=label, notes=notes)
        self.__delete_first_flashcard()
        self.__assert_flashcard_lesson_existence(flashcard, new_lesson)
        self.__assert_flashcard_lesson_inexistence(flashcard, old_lesson)

    def test_edit_parent_flashcard(self):
        label = 'Apple'
        notes = 'Fruits'
        new_lesson = self.go_to_lessons_page_of_first_book_with_two_books()
        old_lesson = Lesson.objects.get(title='Hello, world!')
        flashcard = Flashcard.objects.get(label=label, notes=notes)

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        picture = [os.path.join(BASE_DIR, 'static/media/sample_test_image_3.png')]
        new_label = 'Carrot'
        new_notes = 'Vegetables'
        flashcard_type = NAME_PICTURE_ONLY
        orientation = NAME_LANDSCAPE
        is_bordered = True

        self.__edit_first_flashcard(picture, new_label, new_notes, flashcard_type, orientation, is_bordered)

        element = self.browser.find_element_by_link_text('Let\'s Try 2')
        element.click()
        time.sleep(PAGE_LOADING_WAIT_TIME)
        button = self.browser.find_element_by_css_selector('.page-subheader-right > a > .btn')
        button.click()
        time.sleep(PAGE_LOADING_WAIT_TIME)

        self.__assert_flashcard_existence(new_label, new_notes, 'Flashcard with picture only', 'Landscape', is_bordered, new_lesson)

    # Do manual testing on these to be sure.
    def test_download_flashcard(self):
        super().go_to_lessons_page_with_existing_book_lesson_activities_flashcards_and_target_languages()
        button = self.browser.find_element_by_class_name('download-flashcard-button')
        button.click()
        time.sleep(MODAL_TRANSITION_WAIT_TIME)
        super().assert_download_did_not_fail()

    def test_download_all_flashcards(self):
        super().go_to_lessons_page_with_existing_book_lesson_activities_flashcards_and_target_languages()
        super().click_button('download-all-flashcards')
        time.sleep(MODAL_TRANSITION_WAIT_TIME)
        super().assert_download_did_not_fail()

    def test_download_target_language(self):
        super().go_to_lessons_page_with_existing_book_lesson_activities_flashcards_and_target_languages()
        button = self.browser.find_element_by_class_name('download-target-language-button')
        button.click()
        time.sleep(MODAL_TRANSITION_WAIT_TIME)
        super().assert_download_did_not_fail()

    def test_download_all_target_languages(self):
        super().go_to_lessons_page_with_existing_book_lesson_activities_flashcards_and_target_languages()
        super().click_button('download-all-target-languages')
        time.sleep(MODAL_TRANSITION_WAIT_TIME)
        super().assert_download_did_not_fail()
