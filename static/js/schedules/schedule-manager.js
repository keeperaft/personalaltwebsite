var SCHEDULE_MANAGER = SCHEDULE_MANAGER || {};

SCHEDULE_MANAGER.populateDropdownValues = function(e) {
	var $schedule_manager_school_year_selected = $('#schedule-manager-school-year').find(':selected'),
		$schedule_manager_start_month_dropdown_cell = $('#schedule-manager-month-dropdown-cell'),
		$schedule_manager_school_dropdown_cell = $('#schedule-manager-school-dropdown-cell'),
		start_month = $schedule_manager_school_year_selected.data('start-month'),
		start_year = $schedule_manager_school_year_selected.data('start-year'),
		end_month = $schedule_manager_school_year_selected.data('end-month'),
		end_year = $schedule_manager_school_year_selected.data('end-year'),
		schools = $schedule_manager_school_year_selected.data('schools'),
		current_langauge = $('#active-language').text(),
		$select = $('<select></select>', {
			'class':'form-control',
			'name':'school'
		});

	if (schools.length > 0) {
		// Populate dropdown for schools
		for(var item in schools) {
			if (current_langauge == 'ja') {
				school_name = schools[item].name_kanji
			}
			else {
				school_name = schools[item].name
			}
			$select.append($('<option></option>', {
				'value':schools[item].id,
				'text':school_name
			}));
		}
	}
	else {
		$select.append($('<option></option>', {
			'value':'0',
			'text':'There are no schools available for the selected school year.'
		}));
		$select.attr('disabled', 'true');
	}
	$schedule_manager_school_dropdown_cell.html($select);
	
	// Calculate the options for month from the given start and end months and years
	$schedule_manager_start_month_dropdown_cell.html(BASE.generateYearMonthDropdown(start_year, end_year, start_month, end_month));
};

SCHEDULE_MANAGER.changeButtonHref = function(e) {
	var $link = $('#view-schedule-link'),
		school_year_id = $('#schedule-manager-school-year').val(),
		school_id = $('#schedule-manager-school-dropdown-cell > select').val(),
		month_year = $('#schedule-manager-month-dropdown-cell > select').val(),
		month_year_arr = month_year.split("-"),
		year = month_year_arr[0],
		month = month_year_arr[1],
		href = '/schedules/view_schedule/'+school_year_id+'/'+school_id+'/'+year+'/'+month;

	$link.attr('href', href);
}

$(document).ready(function(){
	SCHEDULE_MANAGER.populateDropdownValues();
	SCHEDULE_MANAGER.changeButtonHref();
	
	$(document)
		.on('change', '#schedule-manager-school-year', SCHEDULE_MANAGER.populateDropdownValues)
		.on('change', '#schedule-manager-table select', SCHEDULE_MANAGER.changeButtonHref);
});