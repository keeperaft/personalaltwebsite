from django.conf.urls import include, url
from django.contrib import admin
from paw.constants.base import SCHEDULES, LESSONS, SCHOOL_YEARS, ACCOUNTS
from django.conf.urls import (
    handler400, handler403, handler404, handler500
)

handler404 = 'home.views.page_not_found'
handler500 = 'home.views.server_error'

urlpatterns = [
	url(r'^admin', include(admin.site.urls)),
	url(r'^'+SCHEDULES+'/', include('schedules.urls')),
	url(r'^'+LESSONS+'/', include('lessons.urls')),
	url(r'^'+SCHOOL_YEARS+'/', include('schoolyears.urls')),
	url(r'^', include('home.urls')),
]

