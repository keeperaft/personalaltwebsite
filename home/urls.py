from home.constants import *
from paw.methods import Url
from . import views

app_name = 'home'
urlpatterns = []
url_manager = Url(urlpatterns, views)

url_manager.add_url(EXPRESSION_INDEX, INDEX)
url_manager.add_url(EXPRESSION_INDEX_BASE, INDEX)
url_manager.add_url(EXPRESSION_DASHBOARD, INDEX)
url_manager.add_url(EXPRESSION_PRINT_DAY, PRINT_DAY)
url_manager.add_url(EXPRESSION_PRINT_WEEK, PRINT_WEEK)
url_manager.add_url(EXPRESSION_ABOUT, ABOUT)
url_manager.add_url(EXPRESSION_LANGUAGE, LANGUAGE)
url_manager.add_url(EXPRESSION_REMOVE_DEMO_INFO, REMOVE_DEMO_INFO)
url_manager.add_url(EXPRESSION_RESET_DATABASE, RESET_DATABASE)