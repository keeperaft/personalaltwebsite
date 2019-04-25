from django.utils.translation import ugettext_lazy as _
from paw.constants.models import HEX_COLOR_GREEN, HEX_COLOR_BLUE, HEX_COLOR_YELLOW, HEX_COLOR_ORANGE, HEX_COLOR_RED
from schoolyears.constants import HIGH_SCHOOL, JUNIOR_HIGH_SCHOOL, ELEMENTARY_SCHOOL 
 
# Sidebar values
INDEX = 'index'
ADD_CLASS = 'add_class'
EDIT_CLASS = 'edit_class'
ASSIGN_BOOK = 'assign_book'
ADD_SECTION = 'add_section'
VIEW_SECTION = 'view_section'
DELETE_CLASS = 'delete_class'
REASSIGN_BOOK = 'reassign_book'
VIEW_SCHEDULE = 'view_schedule'
DELETE_PERIOD = 'delete_period'
UPDATE_COURSE = 'update_course'
UPDATE_SECTION = 'update_section'
SCHOOL_PERIODS = 'school_periods'
DELETE_SECTION = 'delete_section'
GET_LAST_PERIOD = 'get_last_period'
EDIT_LESSON_HOUR = 'edit_lesson_hour'
SCHEDULE_MANAGER = 'schedule_manager'
SECTIONS_COURSES = 'sections_courses'
ADD_PERIOD_PROFILE = 'add_period_profile'
VIEW_SECTION_PERIOD = 'view_section_period'
ADD_NEW_TIME_PERIOD = 'add_new_time_period'
DELETE_ASSIGNED_BOOK = 'delete_assigned_book'
UPDATE_PERIOD_NUMBER = 'update_period_number'
SCHOOL_PERIOD_SCHOOLS = 'school_period_schools'
UPDATE_PERIOD_PROFILE = 'update_period_profile'
UPDATE_PERIOD_END_TIME = 'update_period_end_time'
VIEW_SECTION_ACTIVITIES = 'view_section_activities'
UPDATE_PERIOD_START_TIME = 'update_period_start_time'
EDIT_SCHEDULE_PERIOD_PROFILE = 'edit_schedule_period_profile'

MAX_PERIOD_PROFILES = 7
MAX_TIME_PERIODS = 10

EXPRESSION_INDEX = r'^$'
EXPRESSION_ADD_CLASS = r'^'+ADD_CLASS+'$'
EXPRESSION_EDIT_CLASS = r'^'+EDIT_CLASS+'$'
EXPRESSION_ADD_SECTION = r'^'+ADD_SECTION+'$'
EXPRESSION_ASSIGN_BOOK = r'^'+ASSIGN_BOOK+'$'
EXPRESSION_DELETE_PERIOD = r'^'+DELETE_PERIOD+'$'
EXPRESSION_REASSIGN_BOOK = r'^'+REASSIGN_BOOK+'$'
EXPRESSION_UPDATE_COURSE = r'^'+UPDATE_COURSE+'$'
EXPRESSION_UPDATE_SECTION = r'^'+UPDATE_SECTION+'/(?P<field>[a-z_]+)$'
EXPRESSION_SCHOOL_PERIODS = r'^'+SCHOOL_PERIODS+'$'
EXPRESSION_DELETE_SECTION = r'^'+DELETE_SECTION+'/(?P<section_id>[0-9_]+)$'
EXPRESSION_GET_LAST_PERIOD = r'^'+GET_LAST_PERIOD+'$'
EXPRESSION_EDIT_LESSON_HOUR = r'^'+EDIT_LESSON_HOUR+'$'
EXPRESSION_SCHEDULE_MANAGER = r'^'+SCHEDULE_MANAGER+'$'
EXPRESSION_SECTIONS_COURSES = r'^'+SECTIONS_COURSES+'$'
EXPRESSION_ADD_PERIOD_PROFILE = r'^'+ADD_PERIOD_PROFILE+'$'
EXPRESSION_ADD_NEW_TIME_PERIOD = r'^'+ADD_NEW_TIME_PERIOD+'$'
EXPRESSION_UPDATE_PERIOD_NUMBER = r'^'+UPDATE_PERIOD_NUMBER+'$'
EXPRESSION_UPDATE_PERIOD_PROFILE = r'^'+UPDATE_PERIOD_PROFILE+'$'
EXPRESSION_UPDATE_PERIOD_END_TIME = r'^'+UPDATE_PERIOD_END_TIME+'$'
EXPRESSION_UPDATE_PERIOD_START_TIME = r'^'+UPDATE_PERIOD_START_TIME+'$'
EXPRESSION_DELETE_CLASS = r'^'+DELETE_CLASS+'/(?P<section_period_id>[0-9_]+)$'
EXPRESSION_EDIT_SCHEDULE_PERIOD_PROFILE = r'^'+EDIT_SCHEDULE_PERIOD_PROFILE+'$'
EXPRESSION_VIEW_SECTION_ACTIVITIES = r'^'+VIEW_SECTION_ACTIVITIES+'/(?P<section_id>[0-9_]+)$'
EXPRESSION_DELETE_ASSIGNED_BOOK = r'^'+DELETE_ASSIGNED_BOOK+'/(?P<school_section_course_id>[0-9]+)/(?P<school_section_id>[0-9]+)$'
EXPRESSION_VIEW_SECTION = r'^'+VIEW_SECTION+'/(?P<school_section_id>[0-9]+)$'
EXPRESSION_SCHOOL_PERIOD_SCHOOL_ID = r'^'+SCHOOL_PERIODS+'/(?P<school_id>[0-9]+)$'
EXPRESSION_SECTIONS_COURSES_SCHOOL_ID = r'^'+SECTIONS_COURSES+'/(?P<school_id>[0-9]+)$'
EXPRESSION_VIEW_SECTION_PERIOD = r'^'+VIEW_SECTION_PERIOD+'/(?P<section_period_id>[0-9]+)$'
EXPRESSION_VIEW_SCHEDULE = r'^'+VIEW_SCHEDULE+'/(?P<school_year_id>[0-9]+)/(?P<school_id>[0-9]+)/(?P<year>[0-9]+)/(?P<month>[0-9]+)$'

PERIOD_TYPE_TEXT = _('This schedule type is used on:')
NAME_PERIOD = _('Period Name')
NAME_TEACHER = _('Teacher')
NAME_NOTES = _('Notes')
NAME_STUDENT_COUNT = _('Student Count')
NAME_LESSON_NUMBER = _('Lesson Number')
NAME_HOUR_NUMBER = _('Hour Number')
NAME_PERIOD_PROFILE = _('Period Profile')

PERIOD_TYPE_NORMAL = 'NORM'
PERIOD_TYPE_MONDAY = 'MOND'
PERIOD_TYPE_WEDNESDAY = 'WEDN'
PERIOD_TYPE_SPECIAL = 'SPEC'
PERIOD_TYPE_SATURDAY = 'SATU'

NAME_PERIOD_TYPE_NORMAL = _('Normal days')
NAME_PERIOD_TYPE_MONDAY = _('Mondays')
NAME_PERIOD_TYPE_WEDNESDAY = _('Wednesdays')
NAME_PERIOD_TYPE_SPECIAL = _('Special days')
NAME_PERIOD_TYPE_SATURDAY = _('Saturdays')

MSG_ERR_SECTION_DNE = _('This section does not exist.')
MSG_ERR_SELECT_SCHOOL = _('Please select a school from the dropdown.')
MSG_ERR_UPDATE_COURSE = _('Please select a book from the dropdown.')
MSG_ERR_SCHEDULE_INCOMPLETE = _('Please select the correct values for school, school year, and month.')
MSG_ERR_CANNOT_ADD_CLASS_WITHOUT_SECTION = _('Adding a new class without its section is not possible.')
MSG_ERR_TOO_MANY_SECTIONS = _('Users can add a maximum of 8 sections.')
MSG_ERR_TOO_MANY_PERIOD_PROFILES = _('Users can add a maximum of 7 period profiles.')
MSG_ERR_TOO_MANY_TIME_PERIODS = _('Users can add a maximum of 10 time periods.')

MSG_DELETE_CLASS = _('The class has been successfully deleted.')
MSG_EDIT_PERIOD_PROFILE_DAY = _('The period profile for the specified day has been successfully updated.')
MSG_UPDATE_SECTION = _('The section has been successfully updated.')
MSG_UPDATE_SECTION_COUNT = _('The section count has been successfully updated.')
MSG_UPDATE_COURSE = _('The book has been successfully updated.')
MSG_ADD_PERIOD_PROFILE = _('The period profile has been successfully added.')
MSG_UPDATE_PERIOD_PROFILE = _('The period profile has been successfully updated.')
MSG_ADD_CLASS = _('The class has been successfully added to the schedule.')
MSG_EDIT_LESSON_HOUR = _('The lesson number and hour number has been successfully updated.')
MSG_ASSIGN_BOOK = _('The specified book has been successfully assigned to the specified year level.')
MSG_REASSIGN_BOOK = _('The specified book to the specified year level has been successfully re-assigned.')
MSG_DELETE_ASSIGNED_BOOK = _('The specified book to the specified year level has been successfully deleted.')
MSG_DELETE_SECTION = _('The specified section has been successfully deleted.')
MSG_ERR_DELETE_LAST_SECTION = _('The section could not be deleted because it is the last section.')
MSG_ADD_SECTION = _('The section has been successfully added.')

NAME_SCHEDULE_MANAGER = _('Schedule Manager')
NAME_SECTIONS_COURSES = _('Year Level Manager')
NAME_SCHOOL_PERIODS = _('School Periods')

PERIOD_TYPES = (
    (PERIOD_TYPE_NORMAL, NAME_PERIOD_TYPE_NORMAL),
    (PERIOD_TYPE_MONDAY, NAME_PERIOD_TYPE_MONDAY),
    (PERIOD_TYPE_WEDNESDAY, NAME_PERIOD_TYPE_WEDNESDAY),
    (PERIOD_TYPE_SPECIAL, NAME_PERIOD_TYPE_SPECIAL),
    (PERIOD_TYPE_SATURDAY, NAME_PERIOD_TYPE_SATURDAY),
)

PERIOD_TYPE_COLORS = {
    PERIOD_TYPE_NORMAL: HEX_COLOR_GREEN,
    PERIOD_TYPE_MONDAY: HEX_COLOR_BLUE,
    PERIOD_TYPE_WEDNESDAY: HEX_COLOR_YELLOW,
    PERIOD_TYPE_SPECIAL: HEX_COLOR_ORANGE,
    PERIOD_TYPE_SATURDAY: HEX_COLOR_RED
}

ALL_SCHOOL_PERIODS = {} 

NAME_NORMAL_SCHEDULE = _('Normal Schedule')
NAME_MONDAY_SCHEDULE = _('Monday Schedule')
NAME_WEDNESDAY_SCHEDULE = _('Wednesday Schedule')

ALL_SCHOOL_PERIODS[ELEMENTARY_SCHOOL] = [{ 
    'period_name': NAME_NORMAL_SCHEDULE, 
    'period_type': PERIOD_TYPE_NORMAL, 
    'periods': [
        {'number': 1, 'start': '8:50', 'end': '9:35'},
        {'number': 2, 'start': '9:40', 'end': '10:25'},
        {'number': 3, 'start': '10:45', 'end': '11:30'},
        {'number': 4, 'start': '11:35', 'end': '12:20'},
        {'number': 5, 'start': '13:50', 'end': '14:35'},
        {'number': 6, 'start': '14:40', 'end': '15:25'},
    ], 
}, { 
    'period_name': NAME_MONDAY_SCHEDULE, 
    'period_type': PERIOD_TYPE_MONDAY, 
    'periods': [
        {'number': 1, 'start': '8:50', 'end': '9:35'},
        {'number': 2, 'start': '9:40', 'end': '10:25'},
        {'number': 3, 'start': '10:45', 'end': '11:30'},
        {'number': 4, 'start': '11:35', 'end': '12:20'},
        {'number': 5, 'start': '13:50', 'end': '14:35'},
    ], 
}, { 
    'period_name': NAME_WEDNESDAY_SCHEDULE, 
    'period_type': PERIOD_TYPE_WEDNESDAY, 
    'periods': [
        {'number': 1, 'start': '8:50', 'end': '9:35'},
        {'number': 2, 'start': '9:40', 'end': '10:25'},
        {'number': 3, 'start': '10:45', 'end': '11:30'},
    ], 
}] 

ALL_SCHOOL_PERIODS[JUNIOR_HIGH_SCHOOL] = [{ 
    'period_name': NAME_NORMAL_SCHEDULE, 
    'period_type': PERIOD_TYPE_NORMAL, 
    'periods': [
        {'number': 1, 'start': '8:50', 'end': '9:40'},
        {'number': 2, 'start': '9:50', 'end': '10:40'},
        {'number': 3, 'start': '10:50', 'end': '11:40'},
        {'number': 4, 'start': '11:50', 'end': '12:40'},
        {'number': 5, 'start': '13:30', 'end': '14:20'},
        {'number': 6, 'start': '14:30', 'end': '15:20'},
    ], 
}]


ALL_SCHOOL_PERIODS[HIGH_SCHOOL] = [{ 
    'period_name': NAME_NORMAL_SCHEDULE, 
    'period_type': PERIOD_TYPE_NORMAL, 
    'periods': [
        {'number': 1, 'start': '8:50', 'end': '9:40'},
        {'number': 2, 'start': '9:50', 'end': '10:40'},
        {'number': 3, 'start': '10:50', 'end': '11:40'},
        {'number': 4, 'start': '11:50', 'end': '12:40'},
        {'number': 5, 'start': '13:30', 'end': '14:20'},
        {'number': 6, 'start': '14:30', 'end': '15:20'},
    ], 
}]
