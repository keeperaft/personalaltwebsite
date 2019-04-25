import io
import zipfile

from django.conf import settings
from django.contrib import messages
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, Http404
from django.views.decorators.http import require_POST
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from home.pdf import print_lesson_plan_pdf, download_flashcard_pdf, download_all_flashcards_pdf, \
    download_target_language_pdf, download_all_target_languages_pdf
from lessons.forms import *
from lessons.models import *
from lessons.constants import *
from paw.constants.base import MODAL_ID
from paw.constants.base import NAME, URL, IS_SELECTED, SUBITEMS, LESSONS
from paw.methods import render_page, get_value_of_bootstrap_switch_in_post


def lessons_render_page(request,
    page='lessons-index',
    context={},
    selected_sidebar=COURSES,
    selected_subitem=False):

    # Sidebar
    courses = {
        NAME: NAME_COURSES,
        URL: 'lessons/'+COURSES,
        IS_SELECTED: False,
        MODAL_ID: None,
    }
    generic_activities = {
        NAME: NAME_GENERIC_ACTIVITIES,
        URL: 'lessons/'+GENERIC_ACTIVITIES,
        IS_SELECTED: False,
        MODAL_ID: None,
    }
    lesson_plans = {
        NAME: NAME_LESSON_PLANS,
        URL: 'lessons/'+LESSON_PLANS,
        IS_SELECTED: False,
        MODAL_ID: None,
    }
    flashcard_manager = {
        NAME: NAME_FLASHCARD_MANAGER,
        URL: 'lessons/'+FLASHCARD_MANAGER,
        IS_SELECTED: False,
        MODAL_ID: None
    }
    generic_lesson_plans = {
        NAME: NAME_GENERIC_LESSON_PLANS,
        URL: 'lessons/'+GENERIC_LESSON_PLANS,
        IS_SELECTED: False,
        MODAL_ID: None
    }

    courses[SUBITEMS] = Course.objects.get_sidebar_courses(selected_subitem)
    context['add_course_form'] = CourseForm()

    sidebar = OrderedDict()
    sidebar[COURSES] = courses
    sidebar[GENERIC_ACTIVITIES] = generic_activities
    sidebar[GENERIC_LESSON_PLANS] = generic_lesson_plans
    sidebar[LESSON_PLANS] = lesson_plans
    sidebar[FLASHCARD_MANAGER] = flashcard_manager

    sidebar[selected_sidebar][IS_SELECTED] = True

    return render_page(request,
       page,
       context,
       sidebar=sidebar,
       selected_menu=LESSONS)

def index(request, course_id=None):
    context = {}

    # If course_id is not None, retrieve its corresponding database entry.
    # Else, get the first available course.
    course = get_object_or_404(Course, pk=course_id) if course_id != None else Course.objects.order_by('course_name').first()
    course_id = course.id if course is not None else None # In the event that course_id was none
    all_lessons = None
    edit_course_form = None

    if course is not None:
        all_lessons = Lesson.objects.filter(course=course).order_by('lesson_number')
        for lesson in all_lessons:
            lesson.form = LessonForm(instance=lesson)
        edit_course_form = CourseForm(instance=course)

    context['add_lesson_form'] = LessonForm()
    context['course'] = course
    context['all_lessons'] = all_lessons
    context['edit_course_form'] = edit_course_form

    return lessons_render_page(request,
       page=COURSES,
       context=context,
       selected_sidebar=COURSES,
       selected_subitem=course_id)

def view_lesson(request, course_id, lesson_id):
    context = {}

    lesson = get_object_or_404(Lesson, pk=lesson_id)
    lesson.book_activities = Activity.objects.filter(activity_source_type=BOOK_BOUND, lesson=lesson).order_by('activity_name')
    lesson.free_activities = Activity.objects.filter(activity_source_type=BOOK_FREE, lesson=lesson).order_by('activity_name')
    lesson.existing_flashcard_dropdown = FlashcardLesson.objects.exclude(lesson=lesson).values('flashcard__id', 'flashcard__label', 'flashcard__notes', 'lesson__lesson_number', 'lesson__course__course_code').order_by('flashcard__label')

    lesson.flashcard_lessons = FlashcardLesson.objects.filter(lesson=lesson).order_by('flashcard__label')      
    lesson.target_languages = TargetLanguage.objects.filter(lesson=lesson).order_by('target_language')
    
    LessonManager().modify_activities(lesson.book_activities)
    LessonManager().modify_activities(lesson.free_activities)

    context['lesson'] = lesson
    context['course'] = get_object_or_404(Course, pk=course_id)

    return lessons_render_page(request,
       page=VIEW_LESSON,
       context=context,
       selected_sidebar=COURSES,
       selected_subitem=course_id)

def download_file(request, activity_file_id):
    activity_file = get_object_or_404(ActivityFile, pk=activity_file_id)
    file_path = os.path.join(settings.MEDIA_ROOT, str(activity_file.activity_file))
    with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename='+slugify(activity_file.original_filename)
        return response

def generic_lesson_plans(request, topic_id=None):
    context = {}
    context['topics'] = Topic.objects.all().order_by('name')
    context['add_topic_form'] = TopicForm()
    edit_topic_form = None
    selected_topic = None
    add_hour_form = None
    all_hours = None
    lesson_title = None

    if topic_id is not None:
        selected_topic = get_object_or_404(Topic, pk=topic_id)
        all_hours = LessonPlan.objects.get_all_hours_from_topic(topic=selected_topic)
        add_hour_form = LessonPlanForm(lessons=None)
        lesson_title = selected_topic.name
        edit_topic_form = TopicForm(instance=selected_topic)

    context['selected_topic'] = selected_topic
    context['add_hour_form'] = add_hour_form
    context['all_hours'] = all_hours
    context['lesson_title'] = lesson_title
    context['edit_topic_form'] = edit_topic_form
    context['add_lesson_plan_url'] = '/lessons/add_generic_lesson_plan'
    context['page_header_left_col_count'] = 6
    context['page_header_right_col_count'] = 6

    return lessons_render_page(request,
       page=GENERIC_LESSON_PLANS,
       context=context,
       selected_sidebar=GENERIC_LESSON_PLANS)

def download_all_flashcards(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=int(lesson_id))
    return download_all_flashcards_pdf(lesson)

def download_flashcard(request, flashcard_id):
    flashcard = get_object_or_404(Flashcard, pk=flashcard_id)
    return download_flashcard_pdf(flashcard)

def download_all(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    all_files = ActivityFile.objects.filter(activity=activity)
    zippable_files = []
    for file in all_files:
        zippable_files.append(os.path.join(settings.MEDIA_ROOT, static('/media/'+str(file.activity_file))))

    zip_subdir = 'all-activity-files'
    zip_filename = 'all-activity-files.zip'
    
    # Open BytesIO to grab in-memory ZIP contents
    bytes_io = io.BytesIO()

    # The zip compressor
    zip_file = zipfile.ZipFile(bytes_io, "w")

    for fpath in zippable_files:
        # Calculate path for file in zip
        fdir, fname = os.path.split(fpath)
        zip_path = os.path.join(zip_subdir, fname)

        # Add file, at correct path
        zip_file.write(str(fpath), str(zip_path))

    # Must close zip for all contents to be written
    zip_file.close()

    # Grab ZIP file from in-memory, make response with correct MIME-type and correct content-disposition
    response = HttpResponse(bytes_io.getvalue(), content_type="application/x-zip-compressed")
    response['Content-Disposition'] = 'attachment; filename='+zip_filename
    return response

def generic_activities(request):
    context = {}
    context['add_activity_form'] = GenericActivityForm()
    context['all_activities'] = Activity.objects.get_all_generic_activities()

    return lessons_render_page(request,
       page=GENERIC_ACTIVITIES,
       context=context,
       selected_sidebar=GENERIC_ACTIVITIES)

def lesson_plans(request, lesson_id=None):
    context = {}
    context['all_courses'] = Course.objects.get_courses_and_lessons()
    all_hours = None
    add_hour_form = None
    selected_course = None
    selected_lesson = None
    lesson_title = None

    if lesson_id is not None and lesson_id != 0:
        selected_lesson = get_object_or_404(Lesson, pk=lesson_id)
        selected_course = selected_lesson.course
        all_hours = LessonPlan.objects.get_all_hours_from_lesson(selected_lesson)
        add_hour_form = LessonPlanForm(lessons=[selected_lesson])
        if selected_course.course_name and selected_lesson.lesson_number:
            lesson_title = _("%(course_name)s, Lesson %(lesson_number)d ") % {
                'course_name': selected_course.course_name, 
                'lesson_number': selected_lesson.lesson_number}

    context['all_hours'] = all_hours
    context['add_hour_form'] = add_hour_form
    context['selected_course'] = selected_course
    context['selected_lesson'] = selected_lesson
    context['lesson_title'] = lesson_title
    context['add_lesson_plan_url'] = '/lessons/add_lesson_plan'
    context['page_header_left_col_count'] = 9
    context['page_header_right_col_count'] = 3

    return lessons_render_page(request,
       page=LESSON_PLANS,
       context=context,
       selected_sidebar=LESSON_PLANS)
    
def print_lesson_plan(request, lesson_plan_id):
    return print_lesson_plan_pdf(lesson_plan_id)

def __get_time_portion_value(request, time_portion):
    activity_id = int(request.POST[time_portion]) if time_portion in request.POST else None
    if activity_id is not None and activity_id != 0:
        return Activity.objects.get(pk=activity_id)
    return None

def view_activity(request, activity_id=None):
    context = {}

    if activity_id is not None:
        activity = get_object_or_404(Activity, pk=activity_id)
        activity.files = ActivityFile.objects.filter(activity=activity)
        activity.set_readable_portion_type()
        activity.existing_file_dropdown = ActivityFile.objects.exclude(activity=activity).values('id', 'activity__activity_name', 'original_filename').order_by('activity__activity_name')
        for file in activity.files:
            file.edit_form = FileForm(instance=file)
    else:
        activity = Activity.objects.first()

    if activity is None:
        messages.error(request, MSG_ERR_NO_ACTIVITY)
        return redirect('/lessons/courses/')

    activity.set_readable_skill_type()
    activity.add_file_form = FileForm()
    context['activity'] = activity

    return lessons_render_page(request,
       page=VIEW_ACTIVITY,
       context=context)

def download_target_language(request, target_language_id):
    target_language = get_object_or_404(TargetLanguage, pk=target_language_id)
    return download_target_language_pdf(target_language)

def download_all_target_languages(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=int(lesson_id))
    return download_all_target_languages_pdf(lesson)
        
def flashcard_manager(request):
    context = {}
    context['add_flashcard_form'] = FlashcardForm()
    context['add_target_language_form'] = TargetLanguageForm()

    return lessons_render_page(request,
       page=FLASHCARD_MANAGER,
       context=context,
       selected_sidebar=FLASHCARD_MANAGER)

def search_flashcard(request, search_term):
    context = {}
    context['add_flashcard_form'] = FlashcardForm()
    context['add_target_language_form'] = TargetLanguageForm()

    if search_term is not None:
        if search_term.strip() is not '':
            context['flashcard_lessons'] = Flashcard.objects.search_flashcard(search_term)
            context['target_languages'] = TargetLanguage.objects.search_target_language(search_term)
            context['display_lesson_information'] = True
            context['search_term'] = search_term
        
        return lessons_render_page(request,
            page=FLASHCARD_MANAGER,
            context=context,
            selected_sidebar=FLASHCARD_MANAGER)
    else:
        raise Http404("URL Not Found")

def generate_flashcard(request):
    form = FlashcardForm(request.POST, request.FILES)

    if form.is_valid():
        flashcard = form.save(commit=False)
        return download_flashcard_pdf(flashcard, picture=request.FILES['picture'])
    else:
        raise Http404("URL Not Found")

def generate_target_language(request):
    form = TargetLanguageForm(request.POST)

    if form.is_valid():
        target_language = form.save(commit=False)
        return download_target_language_pdf(target_language, does_lesson_exist=False)
    else:
        raise Http404("URL Not Found")
