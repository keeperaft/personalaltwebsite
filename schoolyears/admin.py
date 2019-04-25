from django.contrib import admin
from .models import *

admin.site.register(SchoolYear)
admin.site.register(School)
admin.site.register(YearlySchedule)
admin.site.register(SpecialYearlySchedule)
admin.site.register(Node)
admin.site.register(RouteInfo)
admin.site.register(SchoolRoute)
admin.site.register(Path)