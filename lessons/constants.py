from django.utils.translation import ugettext_lazy as _

from paw.constants.models import NAME_BOOK_FREE, NAME_BOOK_BOUND, NAME_VOCABULARY, NAME_CONVERSATION, NAME_LISTENING, \
    NAME_OTHER_SKILLS, NAME_TARGET_LANGUAGE_RED, NAME_TARGET_LANGUAGE_BLUE, NAME_PORTRAIT, NAME_LANDSCAPE, \
    NAME_PICTURE_LABEL, NAME_PICTURE_ONLY, NAME_FRONT_BACK

# Sidebar values
INDEX = 'index'
COURSES = 'courses'
HANDOUTS = 'handouts'
ADD_FILE = 'add_file'
ADD_TOPIC = 'add_topic'
EDIT_FILE = 'edit_file'
MATERIALS = 'materials'
FLASHCARDS = 'flashcards'
ADD_COURSE = 'add_course'
ADD_LESSON = 'add_lesson'
EDIT_TOPIC = 'edit_topic'
VIEW_LESSON = 'view_lesson'
DELETE_FILE = 'delete_file'
EDIT_LESSON = 'edit_lesson'
EDIT_COURSE = 'edit_course'
DELETE_TOPIC = 'delete_topic'
DOWNLOAD_ALL = 'download_all'
DELETE_LESSON = 'delete_lesson'
DOWNLOAD_FILE = 'download_file'
LESSON_PLANS = 'lesson_plans'
EDIT_ACTIVITY = 'edit_activity'
VIEW_ACTIVITY = 'view_activity'
ADD_FLASHCARD = 'add_flashcard'
EDIT_FLASHCARD = 'edit_flashcard'
ADD_LESSON_PLAN = 'add_lesson_plan'
SEARCH_FLASHCARD = 'search_flashcard'
DELETE_FLASHCARD = 'delete_flashcard'
EDIT_LESSON_PLAN = 'edit_lesson_plan'
FLASHCARD_MANAGER = 'flashcard_manager'
PRINT_LESSON_PLAN = 'print_lesson_plan'
ADD_EXISTING_FILE = 'add_existing_file'
ADD_BOOK_ACTIVITY = 'add_book_activity'
ADD_FREE_ACTIVITY = 'add_free_activity'
GENERATE_FLASHCARD = 'generate_flashcard'
DOWNLOAD_FLASHCARD = 'download_flashcard'
GENERIC_ACTIVITIES = 'generic_activities'
GENERIC_LESSON_PLANS = 'generic_lesson_plans'
ADD_GENERIC_ACTIVITY = 'add_generic_activity'
EDIT_GENERIC_ACTIVITY = 'edit_generic_activity'
ADD_EXISTING_FLASHCARD = 'add_existing_flashcard'
DOWNLOAD_ALL_FLASHCARDS = 'download_all_flashcards'
ADD_GENERIC_LESSON_PLAN = 'add_generic_lesson_plan'
GENERATE_TARGET_LANGUAGE = 'generate_target_language'

ADD_TARGET_LANGUAGE = 'add_target_language'
EDIT_TARGET_LANGUAGE = 'edit_target_language'
DELETE_TARGET_LANGUAGE = 'delete_target_language'
DOWNLOAD_TARGET_LANGUAGE = 'download_target_language'
DOWNLOAD_ALL_TARGET_LANGUAGES = 'download_all_target_languages'

NAME_ACTIVITY = _('Activity')
NAME_DESCRIPTION = _('Description')
NAME_ACTIVITY_SKILL_TYPE = _('Activity Skill Type')
NAME_MATERIALS = _('Materials')
NAME_ACTIVITY_FILE = _('Activity File')
NAME_NOTES = _('Notes')
NAME_COURSE_NAME = _('Book Name')
NAME_SHORT = _('Short Name')
NAME_BOOK = _('Book')
NAME_TITLE = _('Title')
NAME_ACTIVITY_NAME = _('Activity Name')
NAME_ACTIVITY_PORTION_TYPE = _('Activity Portion Type')
NAME_NAME = _('Name')
NAME_NOTES = _('Notes')
NAME_TARGET_LANGUAGE = _('Target Language')
NAME_COLOR = _('Color')
NAME_FLASHCARD_BORDER = _('Flashcard Border')
NAME_PICTURE = _('Picture')
NAME_LABEL = _('Label')
NAME_NOTES = _('Notes')
NAME_ORIENTATION = _('Orientation')
NAME_FLASHCARD_TYPE = _('Flashcard Type')

GENERIC = 'GE'
GREETING = 'GR'
WARMUP = 'WA'
PRESENTATION = 'PE'
PRACTICE = 'PA'
PRODUCTION = 'PO'
COOLDOWN = 'CO'
ASSESSMENT = 'AS'

NAME_GENERIC = _('Generic/Other')
NAME_GREETING = _('Greeting')
NAME_WARMUP = _('Warmup')
NAME_PRESENTATION = _('Presentation')
NAME_PRACTICE = _('Practice')
NAME_PRODUCTION = _('Production')
NAME_COOLDOWN = _('Cooldown')
NAME_ASSESSMENT = _('Assessment')

ACTIVITY_PORTION_TYPES = (
	(GENERIC, NAME_GENERIC),
	(GREETING, NAME_GREETING),
	(WARMUP, NAME_WARMUP),
	(PRESENTATION, NAME_PRESENTATION),
	(PRACTICE, NAME_PRACTICE),
	(PRODUCTION, NAME_PRODUCTION),
	(COOLDOWN, NAME_COOLDOWN),
	(ASSESSMENT, NAME_ASSESSMENT)
)

VOCABULARY = 'VO'
CONVERSATION = 'CO'
LISTENING = 'LI'
OTHER_SKILLS = 'OT'

ACTIVITY_SKILL_TYPES = (
    (VOCABULARY, NAME_VOCABULARY),
    (CONVERSATION, NAME_CONVERSATION),
    (LISTENING, NAME_LISTENING),
    (OTHER_SKILLS, NAME_OTHER_SKILLS)
)

TARGET_LANGUAGE_RED = 'RE'
TARGET_LANGUAGE_BLUE = 'BL'
TARGET_LANGUAGE_TYPES = (
    (TARGET_LANGUAGE_RED, NAME_TARGET_LANGUAGE_RED),
    (TARGET_LANGUAGE_BLUE, NAME_TARGET_LANGUAGE_BLUE)
)

PORTRAIT = 'PO'
LANDSCAPE = 'LA'
PICTURE_LABEL = 'PL'
PICTURE_ONLY = 'PO'
FRONT_BACK = 'FB'

ORIENTATIONS = (
    (PORTRAIT, NAME_PORTRAIT),
    (LANDSCAPE, NAME_LANDSCAPE),
)
FLASHCARD_TYPES = (
    (PICTURE_LABEL, NAME_PICTURE_LABEL),
    (PICTURE_ONLY, NAME_PICTURE_ONLY),
    (FRONT_BACK, NAME_FRONT_BACK),
)

EXPRESSION_INDEX = r'^$'
EXPRESSION_COURSES = r'^'+COURSES+'$'
EXPRESSION_HANDOUTS = r'^'+HANDOUTS+'$'
EXPRESSION_ADD_FILE = r'^'+ADD_FILE+'$'
EXPRESSION_EDIT_FILE = r'^'+EDIT_FILE+'$'
EXPRESSION_MATERIALS = r'^'+MATERIALS+'$'
EXPRESSION_ADD_TOPIC = r'^'+ADD_TOPIC+'$'
EXPRESSION_FLASHCARDS = r'^'+FLASHCARDS+'$'
EXPRESSION_ADD_COURSE = r'^'+ADD_COURSE+'$'
EXPRESSION_ADD_LESSON = r'^'+ADD_LESSON+'$'
EXPRESSION_EDIT_TOPIC = r'^'+EDIT_TOPIC+'$'
EXPRESSION_EDIT_LESSON = r'^'+EDIT_LESSON+'$'
EXPRESSION_EDIT_COURSE = r'^'+EDIT_COURSE+'$'
EXPRESSION_DELETE_TOPIC = r'^'+DELETE_TOPIC+'/(?P<topic_id>[0-9]+)$'
EXPRESSION_LESSON_PLANS = r'^'+LESSON_PLANS+'$'
EXPRESSION_EDIT_ACTIVITY = r'^'+EDIT_ACTIVITY+'$'
EXPRESSION_ADD_FLASHCARD = r'^'+ADD_FLASHCARD+'$'
EXPRESSION_EDIT_FLASHCARD = r'^'+EDIT_FLASHCARD+'$'
EXPRESSION_ADD_LESSON_PLAN = r'^'+ADD_LESSON_PLAN+'$'
EXPRESSION_EDIT_LESSON_PLAN = r'^'+EDIT_LESSON_PLAN+'$'
EXPRESSION_ADD_BOOK_ACTIVITY = r'^'+ADD_BOOK_ACTIVITY+'$'
EXPRESSION_ADD_FREE_ACTIVITY = r'^'+ADD_FREE_ACTIVITY+'$'
EXPRESSION_ADD_EXISTING_FILE = r'^'+ADD_EXISTING_FILE+'$'
EXPRESSION_FLASHCARD_MANAGER =  r'^'+FLASHCARD_MANAGER+'$'
EXPRESSION_GENERIC_ACTIVITIES = r'^'+GENERIC_ACTIVITIES+'$'
EXPRESSION_GENERATE_FLASHCARD = r'^'+GENERATE_FLASHCARD+'$'
EXPRESSION_ADD_GENERIC_ACTIVITY = r'^'+ADD_GENERIC_ACTIVITY+'$'
EXPRESSION_GENERIC_LESSON_PLANS = r'^'+GENERIC_LESSON_PLANS+'$'
EXPRESSION_GENERIC_LESSON_PLANS_TOPIC_ID = r'^'+GENERIC_LESSON_PLANS+'/(?P<topic_id>[0-9]+)$'
EXPRESSION_EDIT_GENERIC_ACTIVITY = r'^'+EDIT_GENERIC_ACTIVITY+'$'
EXPRESSION_INDEX_COURSE_ID = r'^'+COURSES+'/(?P<course_id>[0-9]+)$'
EXPRESSION_ADD_EXISTING_FLASHCARD =  r'^'+ADD_EXISTING_FLASHCARD+'$'
EXPRESSION_ADD_GENERIC_LESSON_PLAN = r'^'+ADD_GENERIC_LESSON_PLAN+'$'
EXPRESSION_GENERATE_TARGET_LANGUAGE = r'^'+GENERATE_TARGET_LANGUAGE+'$'
EXPRESSION_DOWNLOAD_ALL = r'^'+DOWNLOAD_ALL+'/(?P<activity_id>[0-9]+)$'
EXPRESSION_VIEW_ACTIVITY = r'^'+VIEW_ACTIVITY+'/(?P<activity_id>[0-9]+)$'
EXPRESSION_DELETE_FILE = r'^'+DELETE_FILE+'/(?P<activity_file_id>[0-9]+)$'
EXPRESSION_DOWNLOAD_FILE = r'^'+DOWNLOAD_FILE+'/(?P<activity_file_id>[0-9]+)$'
EXPRESSION_LESSON_PLANS_LESSON_ID = r'^'+LESSON_PLANS+'/(?P<lesson_id>[0-9]+)$'
EXPRESSION_SEARCH_FLASHCARD = r'^'+SEARCH_FLASHCARD+'/(?P<search_term>.*)$'
EXPRESSION_DELETE_FLASHCARD = r'^'+DELETE_FLASHCARD+'/(?P<lesson_id>[0-9]+)/(?P<flashcard_id>[0-9]+)$'
EXPRESSION_PRINT_LESSON_PLAN =  r'^'+PRINT_LESSON_PLAN+'/(?P<lesson_plan_id>[0-9]+)$'
EXPRESSION_VIEW_LESSON = r'^'+VIEW_LESSON+'/(?P<course_id>[0-9]+)/(?P<lesson_id>[0-9]+)$'
EXPRESSION_DELETE_LESSON = r'^'+DELETE_LESSON+'/(?P<lesson_id>[0-9]+)$'
EXPRESSION_DOWNLOAD_FLASHCARD = r'^'+DOWNLOAD_FLASHCARD+'/(?P<flashcard_id>[0-9]+)$'
EXPRESSION_DOWNLOAD_ALL_FLASHCARDS = r'^'+DOWNLOAD_ALL_FLASHCARDS+'/(?P<lesson_id>[0-9]+)$'

EXPRESSION_ADD_TARGET_LANGUAGE = r'^'+ADD_TARGET_LANGUAGE+'$'
EXPRESSION_EDIT_TARGET_LANGUAGE = r'^'+EDIT_TARGET_LANGUAGE+'$'
EXPRESSION_DELETE_TARGET_LANGUAGE = r'^'+DELETE_TARGET_LANGUAGE+'/(?P<target_language_id>[0-9]+)$'
EXPRESSION_DOWNLOAD_TARGET_LANGUAGE = r'^'+DOWNLOAD_TARGET_LANGUAGE+'/(?P<target_language_id>[0-9]+)$'
EXPRESSION_DOWNLOAD_ALL_TARGET_LANGUAGES = r'^'+DOWNLOAD_ALL_TARGET_LANGUAGES+'/(?P<lesson_id>[0-9]+)$'

ADD_COURSE_MODAL_ID = 'add-course'
NAME_ADD_COURSE = _('+ Add New Book')

NAME_COURSES = _('Books')
NAME_MATERIALS = _('Materials')
NAME_FLASHCARDS = _('Flashcards')
NAME_HANDOUTS = _('Handouts')
NAME_GENERIC_ACTIVITIES = _('Generic Activities')
NAME_LESSON_PLANS = _('Lesson Plans')
NAME_FLASHCARD_MANAGER = _('Flashcard Manager')
NAME_GENERIC_LESSON_PLANS = _('Generic Lesson Plans')

MSG_ADD_COURSE = _('A new book has been successfully added.')
MSG_EDIT_COURSE = _('The book has been successfully edited.')
MSG_ADD_LESSON = _('A new lesson has been successfully added.')
MSG_EDIT_LESSON = _('The lesson has been successfully edited.')
MSG_ADD_ACTIVITY = _('The activity has been successfully added.')
MSG_EDIT_ACTIVITY = _('The activity has been successfully edited.')
MSG_ADD_FILE = _('The new file has been successfully added.')
MSG_DELETE_FILE = _('The file has been successfully deleted.')
MSG_ADD_LESSON_PLAN = _('A new lesson plan has been successfully added.')
MSG_EDIT_LESSON_PLAN = _('The lesson plan has been successfully edited.')
MSG_EDIT_FILE = _('The activity file has been successfully edited.')
MSG_ADD_FLASHCARD = _('The flashcard has been successfully added.')
MSG_DELETE_FLASHCARD = _('The flashcard has been successfully deleted.')
MSG_EDIT_FLASHCARD = _('The flashcard has been successfully edited.')
MSG_DELETE_LESSON = _('The specified lesson has been successfully deleted.')
MSG_ADD_TARGET_LANGUAGE = _('The target language has been successfully added.')
MSG_DELETE_TARGET_LANGUAGE = _('The target language has been successfully deleted.')
MSG_EDIT_TARGET_LANGUAGE = _('The target language has been successfully edited.')
MSG_ADD_TOPIC = _('The topic has been successfully added.')
MSG_DELETE_TOPIC = _('The topic has been successfully deleted.')
MSG_EDIT_TOPIC = _('The topic has been successfully edited.')

MSG_ERR_ADD_COURSE = _('There was an error while adding a new book. Please be sure that the fields are correct.')
MSG_ERR_EDIT_COURSE = _('There was an error while editing the book. Please be sure that the fields are correct.')
MSG_ERR_ADD_LESSON = _('There was an error while adding a new lesson. Please be sure that the fields are correct.')
MSG_ERR_EDIT_LESSON = _('There was an error while editing the lesson. Please be sure that the fields are correct.')
MSG_ERR_ADD_ACTIVITY = _('There was an error while adding the activity. Please be sure that the fields are correct.')
MSG_ERR_EDIT_ACTIVITY = _('There was an error while editing the activity. Please be sure that the fields are correct.')
MSG_ERR_ADD_FILE = _('There was an error while adding the new file. Please make sure that the file is not corrupt.')
MSG_ERR_DELETE_FILE = _('There was an error while deleting the file.')
MSG_ERR_ADD_LESSON_PLAN = _('There was an error while adding the lesson plan. Please be sure that the fields are correct.')
MSG_ERR_EDIT_LESSON_PLAN = _('There was an error while editing the lesson plan. Please be sure that the fields are correct.')
MSG_ERR_ADD_FLASHCARD = _('There was an error in adding the new flashcard.')
MSG_ERR_ADD_TARGET_LANGUAGE = _('There was an error in adding the new target language.')
MSG_ERR_ADD_TOPIC = _('There was an error while adding a new topic. Please be sure that the fields are correct.')
MSG_ERR_EDIT_TOPIC = _('There was an error while editing the topic. Please be sure that the fields are correct.')
MSG_ERR_DELETE_TOPIC = _('There was an error while deleting the topic.')
MSG_ERR_NO_ACTIVITY = _('There are no activities found.')

BOOK_FREE = 'BF'
BOOK_BOUND = 'BB'

ACTIVITY_SOURCE_TYPES = (
    (BOOK_FREE, NAME_BOOK_FREE),
    (BOOK_BOUND, NAME_BOOK_BOUND),
)
