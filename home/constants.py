from django.utils.translation import ugettext_lazy as _

# Sidebar values
DASHBOARD = 'dashboard'
UPDATE_USER_SETTINGS = 'update_user_settings'
REIMBURSEMENTS = 'reimbursements'
TIMESHEETS = 'timesheets'
SETTINGS = 'settings'
ABOUT = 'about'
SIGNUP = 'signup'
INDEX = 'index'
LOGIN = 'login'
CHANGE_PASSWORD = 'change_password'
UPDATE_PROFILE = 'update_profile'
LOGOUT = 'logout'
LANGUAGE = 'language'
UPDATE_TIMESHEET_FIELDS = 'update_timesheet_fields'
GENERATE_TIMESHEET_PDF = 'generate_timesheet_pdf'
CHECK_REIMBURSEMENTS = 'check_reimbursements'
LOGIN_VIEW = 'login_view'
LOGOUT_VIEW = 'logout_view'
PRINT_DAY = 'print_day'
PRINT_WEEK = 'print_week'
TEST_SERVER_ERROR = 'test_server_error'
REMOVE_DEMO_INFO = 'remove_demo_info'
RESET_DATABASE = 'reset_database'

# URL patterns
EXPRESSION_REMOVE_DEMO_INFO = r'^'+REMOVE_DEMO_INFO+'$'
EXPRESSION_RESET_DATABASE = r'^'+RESET_DATABASE+'$'
EXPRESSION_PRINT_DAY = r'^' + PRINT_DAY + '$'
EXPRESSION_PRINT_WEEK = r'^' + PRINT_WEEK + '$'
EXPRESSION_DASHBOARD = r'^' + DASHBOARD + '$'
EXPRESSION_REIMBURSEMENTS = r'^' + REIMBURSEMENTS + '$'
EXPRESSION_UPDATE_USER_SETTINGS = r'^' + UPDATE_USER_SETTINGS + '$'
EXPRESSION_TIMESHEETS = r'^' + TIMESHEETS + '$'
EXPRESSION_SETTINGS = r'^' + SETTINGS + '$'
EXPRESSION_SIGNUP = r'^' + SIGNUP + '$'
EXPRESSION_ABOUT = r'^' + ABOUT + '$'
EXPRESSION_LOGIN = r'^' + LOGIN + '$'
EXPRESSION_LOGOUT = r'^' + LOGOUT + '$'
EXPRESSION_CHANGE_PASSWORD = r'^' + CHANGE_PASSWORD + '$'
EXPRESSION_INDEX_BASE = r'^$'
EXPRESSION_INDEX = r'^' + INDEX + '$'
EXPRESSION_SERVER_ERROR = r'^' + TEST_SERVER_ERROR + '$'
EXPRESSION_UPDATE_PROFILE = r'^'+ UPDATE_PROFILE +'/(?P<field>[a-z_]+)/$'
EXPRESSION_LANGUAGE = r'^language/(?P<language_id>[a-z]+)/'
EXPRESSION_UPDATE_TIMESHEET_FIELDS = r'^update_timesheet_fields/$'
EXPRESSION_GENERATE_TIMESHEET_PDF = r'^generate_timesheet_pdf/$'
EXPRESSION_CHECK_REIMBURSEMENTS = r'^check_reimbursements/$'

MSG_ERR_NO_ROUTES_AVAILABLE = _('There are no routes available for the selected school year. Please proceed to the School Years section to add one.')
MSG_ERR_NO_SCHOOL_YEARS = _('This action is not possible if there are no school years available. Please add a school year first by clicking "+ Add New School Year".')
MSG_LOGIN_SUCCESS = _('Login successful. Welcome back!')
MSG_LOGIN_FAILURE = _('The username or password is incorrect. Please try again.')
MSG_LOGOUT_SUCCESS = _('Logout successful.')
MSG_CHANGE_PASSWORD_SUCCESS = _('Your password was successfully updated!')
MSG_CHANGE_PASSWORD_FAILURE = _('Please read the Password Notes.')

NAME_DASHBOARD = _('Dashboard')
NAME_TIMESHEETS = _('Timesheets')
NAME_REIMBURSEMENTS = _('Reimbursements')
NAME_SETTINGS = _('Settings')
NAME_ABOUT = _('About')
