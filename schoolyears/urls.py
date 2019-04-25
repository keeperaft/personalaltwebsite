from schoolyears.constants import *
from . import views
from paw.methods import Url

app_name = 'school_years'
urlpatterns = []
url_manager = Url(urlpatterns, views)

url_manager.add_url(EXPRESSION_INDEX, INDEX)
url_manager.add_url(EXPRESSION_INDEX_ACTIVE_ID, INDEX)
url_manager.add_url(EXPRESSION_SCHOOL_YEAR_SAVE, SCHOOL_YEAR_SAVE)
url_manager.add_url(EXPRESSION_SCHOOL_YEAR_SAVE_ACTIVE_ID, SCHOOL_YEAR_SAVE)
url_manager.add_url(EXPRESSION_ADD_SCHOOL, ADD_SCHOOL)
url_manager.add_url(EXPRESSION_UPDATE_SCHOOL, UPDATE_SCHOOL)
url_manager.add_url(EXPRESSION_EDIT_COLOR, EDIT_COLOR)
url_manager.add_url(EXPRESSION_EDIT_SCHEDULE, EDIT_SCHEDULE)
url_manager.add_url(EXPRESSION_SAVE_CALENDAR, SAVE_CALENDAR)
url_manager.add_url(EXPRESSION_ADD_HOME_STATION, ADD_HOME_STATION)
url_manager.add_url(EXPRESSION_ADD_ROUTE, ADD_ROUTE)
url_manager.add_url(EXPRESSION_UPDATE_PATH, UPDATE_PATH)
url_manager.add_url(EXPRESSION_UPDATE_ROUTE, UPDATE_ROUTE)
url_manager.add_url(EXPRESSION_UPDATE_STATION, UPDATE_STATION)
url_manager.add_url(EXPRESSION_ADD_SCHOOL_YEAR_ROUTE, ADD_SCHOOL_YEAR_ROUTE)
