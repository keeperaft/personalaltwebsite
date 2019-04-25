import calendar

from django.utils import timezone

from schedules.models import SchoolPeriodType, SchoolSection
from schoolyears.constants import *
from schoolyears.managers import *


def get_or_none(model_object, latest_column=None, **kwargs):
    try:
        if latest_column is not None:
            return model_object.objects.filter(**kwargs).latest(latest_column)
    except:
        return None

class SchoolYear(models.Model):
    name = models.CharField(max_length=32)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)
    objects = SchoolYearManager()
    # created_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return " | ".join([self.name, str(self.is_active)])

    def update_active_school_year(self):
        current_date = timezone.now().date()
        if self.start_date <= current_date and current_date <= self.end_date:
            SchoolYear.objects.all().update(is_active=False)
            self.is_active = True
        else:
            self.is_active = False
        self.save()

    def update_name(self):
        if self.end_date <= self.start_date:
            return False

        start_year = self.start_date.year
        end_year = self.end_date.year
        self.name = str(start_year)+' ~ '+str(end_year)

        # If the year is the same but the months are different, the name should be: MO1~MO2 YEAR
        if start_year == end_year:
            start_month = self.start_date.month
            end_month = self.end_date.month
            self.name = calendar.month_abbr[start_month]+' ~ '+calendar.month_abbr[end_month]+' '+str(start_year)

        self.save()
        return True

class School(models.Model):
    school_colors = models.CharField(
        max_length=32,
        choices=SCHOOL_COLORS,
        default=GREEN,
    )

    school_type = models.CharField(
        max_length=32,
        choices=SCHOOL_TYPES,
        default=ELEMENTARY_SCHOOL,
    )

    school_year = models.ForeignKey(SchoolYear, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    name_kanji = models.CharField(max_length=256)
    address = models.CharField(max_length=256)
    contact_number = models.CharField(max_length=16)
    website = models.CharField(max_length=256)
    principal = models.CharField(max_length=128)
    vice_principal = models.CharField(max_length=128)
    english_head_teacher = models.CharField(max_length=128)
    created_at = models.DateField(default=timezone.now)
    objects = SchoolManager()
    # created_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return " | ".join([str(self.id),
                           self.name,
                           self.school_year.name,
                           self.school_type,
                           self.school_colors])

    def get_hex_color(self):
        school_colors = SchoolManager().get_rearranged_colors()
        return school_colors[self.school_colors]

    def get_readable_school_type(self):
        for school_type in SCHOOL_TYPES:
            if school_type[0] == self.school_type:
                return school_type[1]

    def add_default_school_information(self):
        SchoolPeriodType.objects.add_default_period(self)
        SchoolSection.objects.add_default_school_sections(self)

    def save(self, *args, **kwargs):
        should_add_default_period_entries = False

        if self.id is None: # New entry
            should_add_default_period_entries = True
            same_school_instance = get_or_none(School, 'id', name=self.name, name_kanji=self.name_kanji, school_type=self.school_type)

            # Same school found! Prefill it with the latest existing values
            if same_school_instance is not None:
                school_year = self.school_year
                self = same_school_instance
                self.id = None
                self.school_year = school_year

            # Check list of existing colors in the database with the same school year
            retrieved_colors = [color[0] for color in School.objects.filter(school_year=self.school_year).values_list('school_colors')]
            school_colors = [color[0] for color in SCHOOL_COLORS]
            selected_color = GREEN

            if len(retrieved_colors) > 0:
                for color in school_colors:
                    if color not in retrieved_colors:
                        selected_color = color
                        break

            self.school_colors = selected_color

        super(School, self).save(*args, **kwargs)

        if should_add_default_period_entries:
            self.add_default_school_information()

class Node(models.Model):
    name = models.CharField(max_length=128)
    objects = NodeManager()
    # created_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return str(self.name)

class Path(models.Model):
    travel_vehicle_name = models.CharField(max_length=256)
    start_time = models.TimeField()
    end_time = models.TimeField()
    cost = models.IntegerField(default=0)
    # created_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return " | ".join([str(self.travel_vehicle_name), str(self.start_time),
            str(self.end_time), str(self.cost)])

class RouteInfo(models.Model):
    node = models.ForeignKey(Node, related_name='node')
    next_path = models.ForeignKey(Path, related_name='next_path', blank=True, null=True)
    next_route = models.OneToOneField('self',
        blank=True,
        null=True,
        on_delete=None)
    objects = RouteInfoManager()
    # created_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return " || ".join([str(self.node), str(self.next_path)])

class SchoolRoute(models.Model):
    school_year = models.ForeignKey(SchoolYear)
    school = models.ForeignKey(School, null=True)
    source_route_info = models.ForeignKey(RouteInfo, null=True)
    route_name = models.CharField(max_length=128)
    source_name = models.CharField(max_length=128)
    destination_name = models.CharField(max_length=128)
    is_round_trip = models.BooleanField(default=True)
    total_cost = models.IntegerField(default=0)
    is_alt_meeting = models.BooleanField(default=False)
    calculated_total_cost = models.IntegerField(default=0)
    objects = SchoolRouteManager()
    # created_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    
    travel_method = models.CharField(
        max_length=16,
        choices=TRAVEL_METHODS,
        default=TRAVEL_METHOD_ID_NA,
    )

    def __str__(self):
        return " ||| ".join([str(self.school_year.id), str(self.school), 
            str(self.source_route_info), str(self.destination_name), 
            str(self.is_round_trip), str(self.total_cost)])

    def update_total_cost(self):
        route_info = RouteInfo.objects.filter(id=self.source_route_info.id)
        self.total_cost = 0
        while route_info.exists():
            route_info = route_info.get()
            if route_info.next_path is not None:
                self.total_cost += route_info.next_path.cost
                route_info = RouteInfo.objects.filter(id=route_info.next_route.id)
            else:
                break
        self.save()

    def update_destination_name(self):
        route_info = RouteInfo.objects.filter(id=self.source_route_info.id)
        node = None
        while route_info.exists():
            route_info = route_info.get()
            node = Node.objects.get(id=route_info.node.id)
            if route_info.next_route is not None:
                route_info = RouteInfo.objects.filter(id=route_info.next_route.id)
            else:
                break
        self.destination_name = node.name
        self.save()

    def compute_calculated_cost(self):
        self.calculated_total_cost = 0
        if self.is_round_trip:
            self.calculated_total_cost = self.total_cost*2
        else:
            self.calculated_total_cost = self.total_cost
        self.save()

    def get_route_info(self):
        school_route_info = []
        route_info = RouteInfo.objects.filter(id=self.source_route_info.id)

        # NOTE: Route info structure. We need the ID for editing.
        # arr[0] = {'node': 'Toyoda Station', 'next_path': 'JR Chuo Line', 'route_id': 12}
        # arr[1] = {'node': 'Hachioji Station', 'next_path': 'JR Yokohama Line', 'route_id': 13}
        # arr[2] = {'node': 'Hashimoto Station', 'next_path': 'Hashimoto 59 Bus', 'route_id': 14}
        # arr[3] = {'node': 'Tana Bus Terminal', 'next_path': null, 'route_id': 15}

        # Enter the loop if there is any route info attached to the school
        while route_info.exists():
            route_info = route_info.get()
            # Retrieve the important route information: node and next path
            node = Node.objects.get(id=route_info.node.id)
            path = None
            current_route_id = route_info.id
            edit_node_form = self.get_node_form(node)

            if route_info.next_path is not None:
                path = Path.objects.get(id=route_info.next_path.id)
            
            edit_path_form = self.get_path_form(path)
            school_route_info.append({'node': node, 
                'path': path, 
                'route_id': current_route_id,
                'path_form': edit_path_form,
                'node_form': edit_node_form})
    
            # Break from the loop if the linked list is over.
            # At this point, the route_info should be complete.
            if route_info.next_route is None:
                break
            else:
                route_info = RouteInfo.objects.filter(id=route_info.next_route.id)

        return school_route_info

    def get_node_form(self, instance):
        from schoolyears.forms import NodeForm
        return NodeForm(instance=instance)

    def get_path_form(self, instance):
        from schoolyears.forms import PathForm
        return PathForm(instance=instance)

class YearlySchedule(models.Model):
    school_year = models.ForeignKey(SchoolYear, on_delete=models.CASCADE)
    school = models.ForeignKey(School)
    date = models.DateField()
    objects = YearlyScheduleManager()
    # created_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return " || ".join([str(self.school_year), str(self.school), str(self.date)])

class SpecialYearlySchedule(models.Model):
    special_event = models.CharField(
        max_length=32,
        choices=SPECIAL_EVENTS,
        default=KEY_TBA,
    )
    special_colors = models.CharField(
        max_length=32,
        choices=SPECIAL_COLORS,
        default=KEY_TBA,
    )
    school_year = models.ForeignKey(SchoolYear, on_delete=models.CASCADE)
    date = models.DateField()
    objects = SpecialYearlyScheduleManager()
    # created_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    def get_event_name(self):
        for event in SPECIAL_EVENTS:
            if event[0] == self.special_event:
                return event[1]
        return None

    def get_event_color(self):
        for color in SPECIAL_COLORS:
            if color[0] == self.special_event:
                return color[1]
        return None

    def __str__(self):
        return " || ".join([str(self.school_year), str(self.special_event), str(self.date)])
