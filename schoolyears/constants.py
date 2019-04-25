from django.utils.translation import ugettext_lazy as _
from paw.constants.models import NAME_ELEMENTARY_SCHOOL, NAME_JUNIOR_HIGH_SCHOOL, NAME_HIGH_SCHOOL, HEX_COLOR_GREEN, HEX_COLOR_RED, HEX_COLOR_BLUE, HEX_COLOR_YELLOW, HEX_COLOR_ORANGE, HEX_COLOR_PURPLE, HEX_COLOR_TBA, HEX_COLOR_MEETING, HEX_COLOR_WORKDAY

INDEX = 'index'
ADD_SCHOOL = 'add_school'
UPDATE_SCHOOL = 'update_school'
SCHOOL_YEAR_SAVE = 'school_year_save'
EDIT_COLOR = 'edit_color'
EDIT_SCHEDULE = 'edit_schedule'
SAVE_CALENDAR = 'save_calendar'
ADD_HOME_STATION = 'add_home_station'
ADD_SCHOOL_YEAR = 'add_schoolyear'
ADD_SCHOOL_YEAR_MODAL_ID = 'add-schoolyear'
ADD_ROUTE = 'add_route'
UPDATE_ROUTE = 'update_route'
UPDATE_PATH = 'update_path'
UPDATE_STATION = 'update_station'
ADD_SCHOOL_YEAR_ROUTE = 'add_school_year_route'

ELEMENTARY_SCHOOL = 'ES'
JUNIOR_HIGH_SCHOOL = 'JS'
HIGH_SCHOOL = 'HS'

NAME_START_DATE = _('Start date')
NAME_END_DATE = _('End date')
NAME_TRAVEL_VEHICLE = _('Means of Travel')
NAME_START_TIME = _('Start time')
NAME_END_TIME = _('End time')
NAME_COST = _('Cost')
NAME_STATION = _('Station Name')
NAME_IS_ROUND_TRIP = _('Round Trip/One Way')
NAME_IS_ALT_MEETING = _('Is it an ALT Meeting?')
NAME_TOTAL_COST = _('Total Cost (One Way)')
NAME_ROUTE = _('Route')
NAME_SOURCE = _('Source')
NAME_DESTINATION = _('Destination')
NAME_TRAVEL_METHOD = _('Travel Method')

SCHOOL_TYPES = (
    (ELEMENTARY_SCHOOL, NAME_ELEMENTARY_SCHOOL),
    (JUNIOR_HIGH_SCHOOL, NAME_JUNIOR_HIGH_SCHOOL),
)

RED = 'RE'
BLUE = 'BL'
GREEN = 'GR'
YELLOW = 'YE'
ORANGE = 'OR'
PURPLE = 'PU'

SCHOOL_COLORS = (
    (GREEN, HEX_COLOR_GREEN),
    (RED, HEX_COLOR_RED),
    (BLUE, HEX_COLOR_BLUE),
    (YELLOW, HEX_COLOR_YELLOW),
    (ORANGE, HEX_COLOR_ORANGE),
    (PURPLE, HEX_COLOR_PURPLE)
)

EXPRESSION_INDEX = r'^$'
EXPRESSION_INDEX_ACTIVE_ID = r'^(?P<active_id>[0-9]+)$'
EXPRESSION_SCHOOL_YEAR_SAVE = r'^school_year_save/$'
EXPRESSION_SCHOOL_YEAR_SAVE_ACTIVE_ID = r'^school_year_save/(?P<active_id>[0-9]+)$'
EXPRESSION_ADD_SCHOOL = r'^add_school/(?P<school_year_id>[0-9]+)$'
EXPRESSION_UPDATE_SCHOOL = r'^update_school/(?P<field>[a-z_]+)/$'
EXPRESSION_EDIT_COLOR = r'^edit_color/$'
EXPRESSION_EDIT_SCHEDULE = r'^edit_schedule/(?P<school_year_id>[0-9]+)$'
EXPRESSION_SAVE_CALENDAR = r'^save_calendar/'
EXPRESSION_ADD_HOME_STATION = r'^add_home_station/'
EXPRESSION_ADD_ROUTE = r'^add_route/'
EXPRESSION_UPDATE_STATION = r'^update_station/'
EXPRESSION_UPDATE_PATH = r'^update_path/'
EXPRESSION_UPDATE_ROUTE = r'^update_route/(?P<field>[a-z_]+)/'
EXPRESSION_ADD_SCHOOL_YEAR_ROUTE = r'^add_school_year_route/'

KEY_TBA = 'TBA'
KEY_MTG = 'MTG'
KEY_WORKDAY = 'WKD'
NAME_TBA = _('TBA')
NAME_MTG = _('ALT Meeting')
NAME_WORKDAY = _('Work day')

SPECIAL_COLORS = (
    (KEY_TBA, HEX_COLOR_TBA),
    (KEY_MTG, HEX_COLOR_MEETING),
    (KEY_WORKDAY, HEX_COLOR_WORKDAY),
)
SPECIAL_EVENTS = (
    (KEY_TBA, NAME_TBA),
    (KEY_MTG, NAME_MTG),
    (KEY_WORKDAY, NAME_WORKDAY),
)

# If you're wondering why the IDs are like that, I got these from my company's dropdown values
TRAVEL_METHOD_ID_NA = '01.Not Selected'
TRAVEL_METHOD_ID_TRAIN = '02.Train'
TRAVEL_METHOD_ID_BUS = '03.Bus'
TRAVEL_METHOD_ID_TRAIN_BUS = '04.Train/Bus'

TRAVEL_METHOD_NAME_NA = 'Not Selected'
TRAVEL_METHOD_NAME_TRAIN = 'Train'
TRAVEL_METHOD_NAME_BUS = 'Bus'
TRAVEL_METHOD_NAME_TRAIN_BUS = 'Train/Bus'

TRAVEL_METHODS = (
    (TRAVEL_METHOD_ID_NA, TRAVEL_METHOD_NAME_NA),
    (TRAVEL_METHOD_ID_TRAIN, TRAVEL_METHOD_NAME_TRAIN),
    (TRAVEL_METHOD_ID_BUS, TRAVEL_METHOD_NAME_BUS),
    (TRAVEL_METHOD_ID_TRAIN_BUS, TRAVEL_METHOD_NAME_TRAIN_BUS),
)

NAME_ADD_SCHOOL_YEAR = _('+ Add New School Year')
NAME_SCHOOL_NAME = _('School Name')
NAME_KANJI_NAME = _('Kanji Name')
NAME_SCHOOL_TYPE = _('School Type')

MSG_ERR_LATER_END_DATE = _('End date must be later than Start date.')
MSG_ERR_ADD_SCHOOL = _('There is an error in adding the new school.')
MSG_ERR_ADD_HOME_STATION = _('There is an error in adding the home station.')
MSG_ERR_ADD_ROUTE = _('There is an error in adding the route.')
MSG_ERR_ADD_ROUTE_COST = _('The value of the cost must be at least 0.')
MSG_SUCCESS_NEW_SCHOOLYEAR = _('A new school year has been successfully added.')
MSG_SUCCESS_EDIT_SCHOOLYEAR = _('The school year has been successfully edited.')
MSG_SUCCESS_EDIT_SCHOOL_COLOR = _('The school color has been successfully edited.')
MSG_SUCCESS_NEW_SCHOOL = _('A new school has been successfully added.')
MSG_SUCCESS_SAVE_CALENDAR = _('Calendar information has been saved.') 
MSG_SUCCESS_ADD_HOME_STATION = _('The home station has been saved.')
MSG_SUCCESS_ADD_ROUTE = _('The new route has been successfully added.')
MSG_SUCCESS_UPDATE_ROUTE = _('The route has been successfully updated.')
MSG_SUCCESS_UPDATE_STATION = _('The station\'s name has been successfully updated.')
MSG_ERR_TOO_MANY_SCHOOLS = _('Users can add a maximum of 6 schools.')
