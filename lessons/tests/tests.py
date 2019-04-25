import os, time
import selenium
from selenium import webdriver
from django.contrib.auth.models import User
from lessons.models import *
from paw.constants.tests import *
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static

from datetime import datetime, timedelta
from django.test import Client
from selenium.webdriver.common.keys import Keys

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class LessonTestMethods(StaticLiveServerTestCase):

    # TO-DO: Make a base test class in paw: paw.tests, containing all methods from setUp to choose_option_from_select
    # TO-DO: 
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

    # User actions
    def click_button(self, button_name):
        self.browser.execute_script("$('button[name="+button_name+"]').click()")

    def click_a_tag(self, tag_id):
        element = self.browser.find_element_by_id(tag_id)
        element.click()

    def click_modal_save_button(self):
        self.browser.execute_script("$('.modal.fade.in .modal-footer .btn-primary').click();")
        time.sleep(PAGE_LOADING_WAIT_TIME)

    def click_toggle_switch(self, selector_id, should_click):
        if should_click:
            self.browser.execute_script("$('.modal.fade.in .bootstrap-switch input#%s').click();"%(selector_id))
            time.sleep(BOOTSTRAP_SWITCH_TRANSITION_WAIT_TIME)

    def type_text_in_input(self, css_selector, input_text):
        element = self.browser.find_element_by_css_selector(css_selector)
        element.clear()
        element.click()
        element.send_keys(input_text)
        
    def choose_option_from_select(self, selector_id, option_text, is_modal=True):
        css_selector = '.modal.fade.in #%s' % (selector_id)
        css_selector_option = '.modal.fade.in #%s > option' % (selector_id)
        if not is_modal:
            css_selector = '#%s' % (selector_id)
            css_selector_option = '#%s > option' % (selector_id)

        dropdown_element = self.browser.find_element_by_css_selector(css_selector)
        dropdown_element.click()

        option_elements = self.browser.find_elements_by_css_selector(css_selector_option)
        for element in option_elements:
            if element.text == option_text:
                element.click()
                break

    def fill_flashcard_modal(self, picture, label, notes, flashcard_type, orientation, is_bordered):
        if picture is not None:
            self.browser.find_element_by_id('id_picture').send_keys(picture)
        if label is not None:
            self.type_text_in_input('.modal.fade.in #id_label', label)
        if notes is not None:
            self.type_text_in_input('.modal.fade.in #id_notes', notes)
        if flashcard_type is not None:
            self.choose_option_from_select('id_flashcard_type', flashcard_type)
        if orientation is not None:
            self.choose_option_from_select('id_orientation', orientation)
        if is_bordered is not None:
            self.click_toggle_switch(selector_id='id_is_bordered', should_click=is_bordered==False)
        self.click_modal_save_button()
        time.sleep(PAGE_LOADING_WAIT_TIME)

    def fill_target_language_modal(self, target_language, notes, color):
        if target_language is not None:
            self.type_text_in_input('.modal.fade.in #id_target_language', target_language)
        if notes is not None:
            self.type_text_in_input('.modal.fade.in #id_notes', notes)
        if color is not None:
            self.choose_option_from_select('id_color', color)
        self.click_modal_save_button()
        time.sleep(PAGE_LOADING_WAIT_TIME)

    def edit_first_target_language(self, target_language, notes, color):
        edit_button = self.browser.find_element_by_css_selector('.edit-target-language-button')
        edit_button.click()
        time.sleep(MODAL_TRANSITION_WAIT_TIME)
        self.fill_target_language_modal(target_language, notes, color)
        
    def delete_first_target_language(self):
        delete_button = self.browser.find_element_by_css_selector('.delete-target-language-button')
        delete_button.click()
        time.sleep(PAGE_LOADING_WAIT_TIME)

    # Assertions used in multiple places
    def assert_download_did_not_fail(self):
        content = self.browser.find_element_by_css_selector('body').text
        self.assertNotIn('Exception Type', content)

    def __assert_activity_title_in_content(self, name, content):
        if name is not None:
             self.assertIn(name, content)

    def assert_lesson_plan_existence(self, greeting, warmup, presentation, practice, production, cooldown, assessment, hour_number):
        self.assertTrue(LessonPlan.objects.filter(
            greeting__activity_name=greeting,
            warmup__activity_name=warmup,
            presentation__activity_name=presentation,
            practice__activity_name=practice,
            production__activity_name=production,
            cooldown__activity_name=cooldown,
            assessment__activity_name=assessment,
            hour_number=hour_number
        ).exists())
        content = self.browser.find_element_by_id('paw-main-content').text
        self.__assert_activity_title_in_content(greeting, content)
        self.__assert_activity_title_in_content(warmup, content)
        self.__assert_activity_title_in_content(presentation, content)
        self.__assert_activity_title_in_content(practice, content)
        self.__assert_activity_title_in_content(production, content)
        self.__assert_activity_title_in_content(cooldown, content)
        self.__assert_activity_title_in_content(assessment, content)

    # Go to certain pages
    def __add_new_course(self, name=None, code=None):
        if name is not None and code is not None:
            new_course = Course(
                course_name=name,
                course_code=code
            )
        else:
            new_course = Course(
                course_name='Let\'s Try 1',
                course_code='LeTr1'
            )
        new_course.save()
        return new_course

    def __add_new_lesson(self, course, lesson_number=None, title=None):
        if lesson_number is not None and title is not None:
            new_lesson = Lesson(
                course = course,
                lesson_number = lesson_number,
                title = title)
            new_lesson.save()
        else:
            new_lesson = Lesson(
                course = course,
                lesson_number = 1,
                title = 'Hello, world!')
            new_lesson.save()
        return new_lesson

    def __add_new_activities(self, lesson):
        free_activity = Activity(
            activity_source_type=BOOK_FREE,
            lesson=lesson,
            activity_skill_type=VOCABULARY,
            activity_name='Keyword Game',
            description='Choose a keyword, and if that keyword is called, the kids, in pairs, should grab that one eraser in the middle of their tables.',
            materials='Eraser',
        )
        free_activity.save()
        book_activity = Activity(
            activity_source_type=BOOK_BOUND,
            lesson=lesson,
            activity_skill_type=CONVERSATION,
            activity_name='Activity, p.23',
            description='Have the kids walk around the classroom, asking their peers what their favorite food is.',
            materials='Pencil',
        )
        book_activity.save()

    def __add_book_lesson_and_activities(self):
        new_course = self.__add_new_course()
        new_lesson = self.__add_new_lesson(new_course)
        self.__add_new_activities(new_lesson)
        return new_lesson

    def __add_book_lesson_activities_and_flashcards(self):
        new_lesson = self.__add_book_lesson_and_activities()
        new_flashcard_1 = Flashcard(
            orientation=PORTRAIT,
            flashcard_type=PICTURE_LABEL,
            picture=os.path.join(settings.MEDIA_ROOT, static('/media/sample_test_image_1.png')),
            label='Soccer',
            notes='Sports',
            is_bordered=True
        )
        new_flashcard_1.save()
        new_flashcard_2 = Flashcard(
            orientation=LANDSCAPE,
            flashcard_type=PICTURE_ONLY,
            picture=os.path.join(settings.MEDIA_ROOT, static('/media/sample_test_image_2.png')),
            label='Apple',
            notes='Fruits',
            is_bordered=True
        )
        new_flashcard_2.save()
        flashcard_lesson_1 = FlashcardLesson(
            flashcard=new_flashcard_1,
            lesson=new_lesson
        )
        flashcard_lesson_1.save()
        flashcard_lesson_2 = FlashcardLesson(
            flashcard=new_flashcard_2,
            lesson=new_lesson
        )
        flashcard_lesson_2.save()
        return new_lesson

    def __add_book_lesson_activities_flashcards_and_target_languages(self):
        new_lesson = self.__add_book_lesson_activities_and_flashcards()
        new_target_language_1 = TargetLanguage(
            target_language='How are you?',
            color=TARGET_LANGUAGE_RED,
            notes='Feelings',
            lesson=new_lesson
        )
        new_target_language_1.save()
        new_target_language_2 = TargetLanguage(
            target_language='I\'m __.',
            color=TARGET_LANGUAGE_BLUE,
            notes='Feelings',
            lesson=new_lesson
        )
        new_target_language_2.save()
        return new_lesson

    def __add_two_books(self):
        self.__add_book_lesson_activities_and_flashcards()
        new_course = self.__add_new_course('Let\'s Try 2', 'LeTr2')
        new_lesson = self.__add_new_lesson(new_course, lesson_number=1, title='Revenge of the Hello World')
        return new_lesson

    def __add_existing_lesson_to_second_book(self, lesson):
        flashcard = Flashcard.objects.filter(label='Apple', notes='Fruits').first()
        new_flashcard_lesson = FlashcardLesson(
            flashcard=flashcard,
            lesson=lesson
        )
        new_flashcard_lesson.save()

    def __go_to_lessons_page(self):
        self.browser.get('%s%s' % (self.live_server_url, '/lessons/'))
        button = self.browser.find_element_by_css_selector('.page-subheader-right > a > .btn')
        button.click()
        time.sleep(PAGE_LOADING_WAIT_TIME)

    def __go_to_lessons_page_of_new_book(self):
        self.browser.get('%s%s' % (self.live_server_url, '/lessons/'))
        element = self.browser.find_element_by_link_text('Let\'s Try 2')
        element.click()
        time.sleep(PAGE_LOADING_WAIT_TIME)
        button = self.browser.find_element_by_css_selector('.page-subheader-right > a > .btn')
        button.click()
        time.sleep(PAGE_LOADING_WAIT_TIME)

    def __go_to_lessons_page_of_old_book(self):
        self.browser.get('%s%s' % (self.live_server_url, '/lessons/'))
        element = self.browser.find_element_by_link_text('Let\'s Try 1')
        element.click()
        time.sleep(PAGE_LOADING_WAIT_TIME)
        button = self.browser.find_element_by_css_selector('.page-subheader-right > a > .btn')
        button.click()
        time.sleep(PAGE_LOADING_WAIT_TIME)

    def go_to_materials_page(self):
        self.browser.get('%s%s' % (self.live_server_url, '/lessons/'))

    def go_to_materials_page_with_existing_book(self):
        self.__add_new_course()
        self.browser.get('%s%s' % (self.live_server_url, '/lessons/'))

    def go_to_materials_page_with_existing_book_and_lesson(self):
        new_course = self.__add_new_course()
        self.__add_new_lesson(new_course)
        self.browser.get('%s%s' % (self.live_server_url, '/lessons/'))

    def go_to_lessons_page_with_existing_book_and_lesson(self):
        self.go_to_materials_page_with_existing_book_and_lesson()
        button = self.browser.find_element_by_css_selector('.page-subheader-right > a > .btn')
        button.click()
        time.sleep(PAGE_LOADING_WAIT_TIME)
        
    def go_to_lessons_page_with_existing_book_lesson_and_activities(self):
        self.__add_book_lesson_and_activities()
        self.__go_to_lessons_page()

    def go_to_lessons_page_with_existing_book_lesson_activities_and_flashcards(self):
        self.__add_book_lesson_activities_and_flashcards()
        self.__go_to_lessons_page()

    def go_to_lessons_page_with_existing_book_lesson_activities_flashcards_and_target_languages(self):
        self.__add_book_lesson_activities_flashcards_and_target_languages()
        self.__go_to_lessons_page()

    def go_to_lessons_page_with_two_books_lessons_and_flashcards(self):
        new_lesson = self.__add_two_books()
        self.__go_to_lessons_page_of_new_book()
        return new_lesson

    def go_to_lessons_page_with_two_books_lessons_and_existing_flashcards(self):
        new_lesson = self.__add_two_books()
        self.__add_existing_lesson_to_second_book(new_lesson)
        self.__go_to_lessons_page_of_new_book()
        return new_lesson

    def go_to_lessons_page_of_first_book_with_two_books(self):
        new_lesson = self.__add_two_books()
        self.__add_existing_lesson_to_second_book(new_lesson)
        self.__go_to_lessons_page_of_old_book()
        return new_lesson

    ######################

    def __add_generic_activity(self):
        new_generic_activity = Activity(
            lesson=None,
            activity_skill_type=VOCABULARY,
            activity_name='Hello Song',
            description='Hello, hello, hello, how are you? I\'m fine, I\'m fine. I\'m fine, thank you, and you?',
            materials='CD',
            activity_portion_type=GREETING,
        )
        new_generic_activity.save()

    def go_to_generic_activities_page(self):
        self.browser.get('%s%s' % (self.live_server_url, '/lessons/generic_activities'))

    def go_to_generic_activities_page_with_a_generic_activity(self):
        self.__add_generic_activity()
        self.browser.get('%s%s' % (self.live_server_url, '/lessons/generic_activities'))
        time.sleep(PAGE_LOADING_WAIT_TIME)
    
    ######################

    def __add_topic(self):
        new_topic = Topic(
            name='Animals',
            notes='Generic topic about animals'
        )
        new_topic.save()
        return new_topic

    def __add_generic_activity_with_name_and_portion_type(self, name, portion_type, materials='CD, Ohajiki Marbles, Cats'):
        new_generic_activity = Activity(
            lesson=None,
            activity_skill_type=VOCABULARY,
            activity_name=name,
            description='A generic description about the activity',
            materials=materials,
            activity_portion_type=portion_type,
        )
        new_generic_activity.save()

    def __add_generic_activity_for_all_parts(self):
        self.__add_generic_activity_with_name_and_portion_type('Hello Song', GREETING)
        self.__add_generic_activity_with_name_and_portion_type('Missing Game', GENERIC, materials='CD, Nametags, Ohajiki Marbles, Bar Magnets, Books, Notebooks, Rulers, Erasers, Pencil Sharpeners, Number Cards, Small Cards')
        self.__add_generic_activity_with_name_and_portion_type('Rainbow Song', WARMUP)
        self.__add_generic_activity_with_name_and_portion_type('Vocabulary Drilling', PRESENTATION)
        self.__add_generic_activity_with_name_and_portion_type('Keyword Game', PRACTICE)
        self.__add_generic_activity_with_name_and_portion_type('Interview Game', PRODUCTION)
        self.__add_generic_activity_with_name_and_portion_type('Signature Count', COOLDOWN)
        self.__add_generic_activity_with_name_and_portion_type('Vocabulary Volunteer', ASSESSMENT)

    def __get_activity(self, portion_type):
        return Activity.objects.get(activity_portion_type=portion_type)

    def __add_lesson_plan(self):
        self.__add_generic_activity_for_all_parts()
        new_lesson_plan = LessonPlan(
            hour_number=1,
            greeting=self.__get_activity(GREETING),
            warmup=self.__get_activity(WARMUP),
            presentation=self.__get_activity(PRESENTATION),
            practice=self.__get_activity(PRACTICE),
            production=self.__get_activity(PRODUCTION),
            cooldown=self.__get_activity(COOLDOWN),
            assessment=self.__get_activity(ASSESSMENT),
            topic=Topic.objects.get(name='Animals'),
        )
        new_lesson_plan.save()

    def go_to_generic_lesson_plans_page(self):
        self.browser.get('%s%s' % (self.live_server_url, '/lessons/generic_lesson_plans'))

    def go_to_generic_lesson_plans_with_topic(self):
        self.__add_topic()
        self.browser.get('%s%s' % (self.live_server_url, '/lessons/generic_lesson_plans'))

    def go_to_generic_lesson_plans_with_all_generic_activities_available(self):
        self.__add_topic()
        self.__add_generic_activity_for_all_parts()
        self.browser.get('%s%s' % (self.live_server_url, '/lessons/generic_lesson_plans'))

    def go_to_generic_lesson_plans_with_some_generic_activites_available(self):
        self.__add_topic()
        self.__add_generic_activity_with_name_and_portion_type('Rainbow Song', WARMUP)
        self.__add_generic_activity_with_name_and_portion_type('Vocabulary Drilling', PRESENTATION)
        self.__add_generic_activity_with_name_and_portion_type('Keyword Game', PRACTICE)
        self.__add_generic_activity_with_name_and_portion_type('Interview Game', PRODUCTION)
        self.__add_generic_activity_with_name_and_portion_type('Signature Count', COOLDOWN)
        self.__add_generic_activity_with_name_and_portion_type('Vocabulary Volunteer', ASSESSMENT)
        self.browser.get('%s%s' % (self.live_server_url, '/lessons/generic_lesson_plans'))

    def go_to_generic_lesson_plans_with_lesson_plan(self):
        self.__add_topic()
        self.__add_lesson_plan()
        self.browser.get('%s%s' % (self.live_server_url, '/lessons/generic_lesson_plans'))

    ######################

    def __add_non_generic_lesson_plan(self, lesson):
        self.__add_generic_activity_for_all_parts()
        new_lesson_plan = LessonPlan(
            hour_number=1,
            greeting=self.__get_activity(GREETING),
            warmup=self.__get_activity(WARMUP),
            presentation=self.__get_activity(PRESENTATION),
            practice=self.__get_activity(PRACTICE),
            production=self.__get_activity(PRODUCTION),
            cooldown=self.__get_activity(COOLDOWN),
            assessment=self.__get_activity(ASSESSMENT),
            lesson=lesson
        )
        new_lesson_plan.save()

    def go_to_lesson_plans_page(self):
        self.browser.get('%s%s' % (self.live_server_url, '/lessons/lesson_plans'))

    def go_to_lesson_plans_page_with_book(self):
        self.__add_new_course()
        self.browser.get('%s%s' % (self.live_server_url, '/lessons/lesson_plans'))

    def go_to_lesson_plans_with_book_activities(self):
        self.__add_book_lesson_and_activities()
        self.__add_generic_activity_for_all_parts()
        self.browser.get('%s%s' % (self.live_server_url, '/lessons/lesson_plans'))

    def go_to_lesson_plans_with_lesson_plan(self):
        lesson = self.__add_book_lesson_and_activities()
        self.__add_non_generic_lesson_plan(lesson)
        self.browser.get('%s%s' % (self.live_server_url, '/lessons/lesson_plans'))

    ######################

    def __add_books_lessons_with_parent_and_child_flashcards(self):
        self.__add_book_lesson_activities_flashcards_and_target_languages()
        new_course = self.__add_new_course('Let\'s Try 2', 'LeTr2')
        new_lesson = self.__add_new_lesson(new_course, lesson_number=1, title='Revenge of the Hello World')
        apple_flashcard = Flashcard.objects.get(label='Apple')
        flashcard_lesson = FlashcardLesson(
            flashcard=apple_flashcard,
            lesson=new_lesson
        )
        flashcard_lesson.save()

    def go_to_flashcard_management_page_with_two_books_and_parent_child_flashcards(self):
        self.__add_books_lessons_with_parent_and_child_flashcards()
        self.browser.get('%s%s' % (self.live_server_url, '/lessons/flashcard_manager'))

    def go_to_flashcard_management_page(self):
        self.browser.get('%s%s' % (self.live_server_url, '/lessons/flashcard_manager'))

    def go_to_flashcard_management_page_with_fruit_target_language(self):
        new_lesson = self.__add_book_lesson_activities_flashcards_and_target_languages()
        new_target_language_1 = TargetLanguage(
            target_language='I like apples.',
            color=TARGET_LANGUAGE_RED,
            notes='Fruits',
            lesson=new_lesson
        )
        new_target_language_1.save()
        self.browser.get('%s%s' % (self.live_server_url, '/lessons/flashcard_manager'))

    def go_to_flashcard_management_page_with_flashcards_and_target_language(self):
        self.__add_book_lesson_activities_flashcards_and_target_languages()
        self.browser.get('%s%s' % (self.live_server_url, '/lessons/flashcard_manager'))

    def go_to_flashcard_management_page_with_flashcards_no_target_language(self):
        self.__add_book_lesson_activities_and_flashcards()
        self.browser.get('%s%s' % (self.live_server_url, '/lessons/flashcard_manager'))

    def go_to_flashcard_management_page_no_flashcards_with_target_language(self):
        new_lesson = self.__add_book_lesson_and_activities()
        new_target_language_1 = TargetLanguage(
            target_language='How are you?',
            color=TARGET_LANGUAGE_RED,
            notes='Feelings',
            lesson=new_lesson
        )
        new_target_language_1.save()
        new_target_language_2 = TargetLanguage(
            target_language='I\'m __.',
            color=TARGET_LANGUAGE_BLUE,
            notes='Feelings',
            lesson=new_lesson
        )
        new_target_language_2.save()
        self.browser.get('%s%s' % (self.live_server_url, '/lessons/flashcard_manager'))
