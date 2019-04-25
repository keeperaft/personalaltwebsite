var SECTIONS_COURSES = SECTIONS_COURSES || {};

SECTIONS_COURSES.populateDropdownValues = function() {
	var $timesheet_school_year_selected = $('#sections-courses-school-year').find(':selected'),
		$timesheet_school_dropdown_cell = $('#sections-courses-school-dropdown-cell'),
		selected_id = $timesheet_school_dropdown_cell.data('selected-id'),
		start_month = $timesheet_school_year_selected.data('start-month'),
		start_year = $timesheet_school_year_selected.data('start-year'),
		end_month = $timesheet_school_year_selected.data('end-month'),
		end_year = $timesheet_school_year_selected.data('end-year'),
		schools = $timesheet_school_year_selected.data('schools');

	$timesheet_school_dropdown_cell.html(BASE.generateSchoolDropdown(schools, selected_id));

	SECTIONS_COURSES.changeSchoolHref();
};

SECTIONS_COURSES.changeSchoolHref = function() {
	var school_id = $('#sections-courses-school-dropdown-cell select').find(':selected').val(),
		href = '/schedules/sections_courses/'+school_id,
		$link = $('#view-school-profile-button');

	$link.attr('href', href);
}

$(document).ready(function(){
	SECTIONS_COURSES.populateDropdownValues();
	SECTIONS_COURSES.changeSchoolHref();

	$(document)
		.on('change', '#sections-courses-school-year', SECTIONS_COURSES.populateDropdownValues)
		.on('change', '#sections-courses-school-dropdown-cell > select', SECTIONS_COURSES.changeSchoolHref);
});