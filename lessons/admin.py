from django.contrib import admin
from .models import *

admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(LessonPlan)
admin.site.register(ActivityFile)
admin.site.register(Activity)
admin.site.register(Flashcard)
admin.site.register(TargetLanguage)
admin.site.register(FlashcardLesson)
admin.site.register(Topic)