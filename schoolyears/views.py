from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages

from paw.constants.base import *
from paw.methods import render_page, get_value_of_bootstrap_switch_in_post
from schoolyears.forms import *
from schoolyears.models import *

def index(request, active_id=0):
    context = {}

    active_id = int(active_id)
    # school_year_info = SchoolYear.objects.get_sidebar_and_selected_school_year(active_id, request.user)
    school_year_info = SchoolYear.objects.get_sidebar_and_selected_school_year(active_id)
    selected_school_year = school_year_info['selected']
    sidebar = school_year_info['sidebar']

    context['json_travel_method_types'] = SchoolRoute.objects.get_json_travel_method_types()  
    context['json_school_types'] = School.objects.get_json_school_types()
    context['school_colors'] = School.objects.get_rearranged_colors()  
    context['selected_school_year'] = selected_school_year
    context['school_year_form'] = SchoolYearForm()
    context['add_route_form'] = AddRouteForm()
    context['add_school_form'] = SchoolForm()
    context['node_form'] = NodeForm()
    context['path_form'] = PathForm()
    context['edit_form'] = None

    # If there is any selected school year:
    if selected_school_year is not None:
        # Retrieve all the schools within the selected school year and arrange its information
        selected_school_year.update_active_school_year()
        all_schools = School.objects.get_schools_with_arranged_school_colors(selected_school_year)

        # Retrieve all the routes within the schoolyear and add it in the all_schools
        for school in all_schools:
            try:
                school_route = SchoolRoute.objects.filter(school=school, school_year=selected_school_year).get()
                school.route_info = school_route.get_route_info()
                school.school_route_id = school_route.id
            except(KeyError, SchoolRoute.DoesNotExist):
                school.route_info = None
                school.school_route_id = None

        context['schedule_json'] = School.objects.get_json_all_schedules(selected_school_year)
        context['info_json'] = School.objects.get_json_event_info(all_schools)
        context['edit_form'] = SchoolYearForm(instance=selected_school_year)
        context['all_schools'] = all_schools

    return render_page(request,
                       'index',
                       context,
                       sidebar=sidebar,
                       selected_menu=SCHOOL_YEARS)

def edit_schedule(request, school_year_id=0):
    context = {}

    all_schools = School.objects.get_schools_with_arranged_school_colors(school_year_id)
    selected_school_year = get_object_or_404(SchoolYear, pk=school_year_id)

    context['special_events'] = SpecialYearlySchedule.objects.get_special_events_key_value_color()
    context['schedule_json'] = School.objects.get_json_all_schedules(selected_school_year)
    context['info_json'] = School.objects.get_json_event_info(all_schools)
    context['selected_school_year'] = selected_school_year
    context['all_schools'] = all_schools

    return render_page(request,
                       'edit-schedule',
                       context,
                       sidebar={},
                       selected_menu=SCHOOL_YEARS)

@require_POST
def save_calendar(request):
    if 'value' in request.POST and request.POST['value'] != '':
        # sample data = {'47':['2017-12-20','2018-01-01'], '50':['2018-01-03'], 'MTG':['2018-01-03']}
        data = json.loads(request.POST['value'])
        school_year = SchoolYear.objects.get(id=request.POST['school_year_id'])
        for school_id in data:
            if school_id.isdigit():
                YearlySchedule.objects.save_schedule(data, school_id, school_year)
            else:
                SpecialYearlySchedule.objects.save_schedule(data, school_id, school_year)
    return JsonResponse({'is_success': True, 'messages': MSG_SUCCESS_SAVE_CALENDAR})

@require_POST
def edit_color(request):
    primary_key = request.POST['id']
    color_key = request.POST['value']
    school_instance = School.objects.filter(pk=primary_key)
    school_instance.update(school_colors=color_key)
    messages.success(request, MSG_SUCCESS_EDIT_SCHOOL_COLOR)
    return JsonResponse({'is_success': True, 'messages': None})

@require_POST
def add_school(request, school_year_id):
    school_year_instance = SchoolYear.objects.get(id=school_year_id)
    form = SchoolForm(request.POST)

    if School.objects.filter(school_year=school_year_instance).count() >= 6:
        return JsonResponse({'is_success': False, 'messages': {'Error': MSG_ERR_TOO_MANY_SCHOOLS}})

    if form.is_valid():
        school_form = form.save(commit=False)
        school_form.school_year = school_year_instance
        school_form.save()
        messages.success(request, MSG_SUCCESS_NEW_SCHOOL)
    else:
        return JsonResponse({'is_success': False, 'messages': {'Error': MSG_ERR_ADD_SCHOOL}})

    return JsonResponse({'is_success': True, 'messages': None})

@require_POST
def update_school(request, field=None):
    primary_key = request.POST['id']
    value = request.POST['value']
    school_instance = School.objects.filter(pk=primary_key)
    school_instance.update(**{field: value})

    if field == 'school_type':
        school_instance_update = School.objects.get(pk=primary_key)
        school_instance_update.add_default_school_information()

    return JsonResponse({'is_success': True, 'messages': None})

@require_POST
def school_year_save(request, active_id=0):
    # Save the school year data
    form = SchoolYearForm(request.POST)
    is_editing = active_id != 0

    # Store the instance of the schoolyear into the form if we're editing
    if is_editing:
        school_year_instance = SchoolYear.objects.get(id=active_id)
        form = SchoolYearForm(request.POST, instance=school_year_instance)

    if form.is_valid():
        school_year_form = form.save(commit=False)
        # school_year_form.created_by = request.user

        # Note that end_year must be later than start_year
        if not school_year_form.update_name():
            return JsonResponse({
                'is_success': False, 
                'messages': {'end_date': MSG_ERR_LATER_END_DATE}
            })            

        school_year_form.update_active_school_year()
        school_year_form.save()

        if is_editing:
            messages.success(request, MSG_SUCCESS_EDIT_SCHOOLYEAR)
        else:
            messages.success(request, MSG_SUCCESS_NEW_SCHOOLYEAR)
        
    else:
        return JsonResponse({'is_success': False, 'messages': form.errors})

    # Load the index page
    return JsonResponse({'is_success': True, 'messages': None})

# This method assumes that there are still no entries for the school-homestation combination
@require_POST
def add_home_station(request):
    form = NodeForm(request.POST)

    if form.is_valid():    
        school_id = request.POST['school_id']
        node_name = request.POST['name']    
        school = School.objects.get(id=school_id)
        school_year_id = request.POST['school_year_id']
        route_name = school.name

        school_year = SchoolYear.objects.get(id=school_year_id)
        node = Node.objects.save_new_node(new_node_name=node_name)
        new_route_info = RouteInfo.objects.save_new_route_info(new_node=node)

        new_school_route = SchoolRoute(
            school_year=school_year,
            school=school,
            source_route_info=new_route_info,
            route_name=route_name,
            source_name=node_name,
            destination_name=route_name,
            is_round_trip=True,
            total_cost=0,
            is_alt_meeting=False,
            calculated_total_cost=0
        )
        new_school_route.save()

        messages.success(request, MSG_SUCCESS_ADD_HOME_STATION)
    else:
        return JsonResponse({'is_success': False, 'messages': {'Error': MSG_ERR_ADD_HOME_STATION}})

    return JsonResponse({'is_success': True, 'messages': None})

@require_POST
def add_route(request):
    try:
        travel_vehicle_name = request.POST['travel_vehicle_name']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        cost = int(request.POST['cost'])
        next_station = request.POST['name']
        route_info_id = request.POST['route_info_id']
        school_route_id = request.POST['school_route_id']

        if cost < 0:
            return JsonResponse({'is_success': False, 'messages': {'Error': MSG_ERR_ADD_ROUTE_COST}})

        node = Node.objects.save_new_node(next_station)
        new_path = Path(travel_vehicle_name=travel_vehicle_name, 
            start_time=start_time, 
            end_time=end_time,
            cost=cost)
        new_path.save()
        new_route_info = RouteInfo.objects.save_new_route_info(node)

        # Update the old route using the route_info_id, adding the new path and new route
        source_route_info = RouteInfo.objects.get(id=route_info_id)
        source_route_info.next_path = new_path
        source_route_info.next_route = new_route_info
        source_route_info.save()

        # Update the total cost and the destination name of the school_route_id if the cost > 0
        school_route = SchoolRoute.objects.get(id=school_route_id)
        school_route.update_total_cost()
        school_route.compute_calculated_cost()
        school_route.update_destination_name()           
        school_route.save()

        messages.success(request, MSG_SUCCESS_ADD_ROUTE)
    except ValidationError:
        return JsonResponse({'is_success': False, 'messages': {'Error': MSG_ERR_ADD_ROUTE}})


    return JsonResponse({'is_success': True, 'messages': None})

@require_POST
def update_path(request):
    travel_vehicle_name = request.POST['travel_vehicle_name']
    start_time = request.POST['start_time']
    end_time = request.POST['end_time']
    cost = int(request.POST['cost'])
    path_id = request.POST['path_id']
    school_route_id = request.POST['school_route_id']

    path = Path.objects.filter(id=path_id)
    old_path_cost = path.get(id=path_id).cost

    path.update(travel_vehicle_name=travel_vehicle_name, 
        start_time=start_time, 
        end_time=end_time,
        cost=cost)

    school_route = SchoolRoute.objects.get(id=school_route_id)
    school_route.update_total_cost()
    school_route.compute_calculated_cost()
    school_route.update_destination_name()

    messages.success(request, MSG_SUCCESS_UPDATE_ROUTE)

    return JsonResponse({'is_success': True, 'messages': None})

@require_POST
def update_station(request):
    name = request.POST['name']
    school_route_id = request.POST['school_route_id']
    route_info_id = request.POST['route_info_id']

    # Save the new node if node name doesn't exist
    node = Node.objects.save_new_node(name)
    school_route = SchoolRoute.objects.get(pk=school_route_id)

    # Update the affected route info
    route_info = RouteInfo.objects.filter(id=route_info_id)
    route_info.update(node=node)
    school_route.update_destination_name()
    messages.success(request, MSG_SUCCESS_UPDATE_STATION)

    return JsonResponse({'is_success': True, 'messages': None})

@require_POST
def update_route(request, field=None):
    primary_key = request.POST['id']
    value = request.POST['value']

    # AJAX sends it as a fucking s t r  i  n      g
    # All the solutions I found online assumed that the values-- 
    # --would only be True or False, so they don't work 
    if value == 'true':
        value = True
    elif value == 'false':
        value = False

    route_instance = SchoolRoute.objects.filter(pk=primary_key)
    route_instance.update(**{field: value})
    return JsonResponse({'is_success': True, 'messages': MSG_SUCCESS_UPDATE_ROUTE})

@require_POST
def add_school_year_route(request):
    form = AddRouteForm(request.POST)

    if form.is_valid():    
        route_name = request.POST['route_name'].strip()
        source_name = request.POST['source_name'].strip()
        destination_name = request.POST['destination_name'].strip()
        school_year_id = request.POST['school_year_id']
        total_cost = int(request.POST['total_cost'])
        travel_method = request.POST['travel_method']

        if total_cost < 0:
            return JsonResponse({'is_success': False, 'messages': {'Error': MSG_ERR_ADD_ROUTE_COST}})

        is_round_trip = get_value_of_bootstrap_switch_in_post(request, 'is_round_trip')
        is_alt_meeting = get_value_of_bootstrap_switch_in_post(request, 'is_alt_meeting')

        # Query the school_year object given the school_year_id
        school_year = SchoolYear.objects.get(id=school_year_id)

        # Calculate for the total cost, given the value of is_round_trip
        calculated_total_cost = total_cost
        if is_round_trip:
            calculated_total_cost = total_cost*2

        new_school_route = SchoolRoute(
            school_year=school_year,
            school=None,
            source_route_info=None,
            route_name=route_name,
            source_name=source_name,
            destination_name=destination_name,
            is_round_trip=is_round_trip,
            total_cost=total_cost,
            is_alt_meeting=is_alt_meeting,
            calculated_total_cost=calculated_total_cost,
            travel_method=travel_method
        )
        new_school_route.save()
    
    else:
        return JsonResponse({'is_success': False, 'messages': {'Error': MSG_ERR_ADD_ROUTE}})
    return JsonResponse({'is_success': True, 'messages': None})