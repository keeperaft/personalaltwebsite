var TIMESHEET = TIMESHEET || {};

TIMESHEET.populateCalendarDropdownValues = function(e, $selector, name, start_month, end_month, start_year, end_year) {
	// Calculate the options for month from the given start and end months and years
	var month_list = BASE.getLocalizedMonthList(),
		month_count = BASE.getMonthCount(start_year, end_year, start_month, end_month),						
		$select = $('<select></select>', {
			'class':'form-control',
			'name':name
		});

	for(var i=0; i<month_count; i++) {
		var month_index = start_month + i - 1,
			name_year = start_year + Math.floor(month_index/12),
			name_month = month_list[month_index%12],
			value = name_year+'-'+((month_index%12)+1),
			name_month_year = name_month+' '+name_year;
		$select.append($('<option></option>', {
			'value':value,
			'text':name_month_year
		}));
	}

	$selector.html($select);
};

TIMESHEET.populateDropdownValues = function(e) {
	var $timesheet_school_year_selected = $('#timesheet-school-year').find(':selected'),
		$timesheet_start_month_dropdown_cell = $('#timesheet-start-month-dropdown-cell'),
		$timesheet_school_dropdown_cell = $('#timesheet-school-dropdown-cell'),
		start_month = $timesheet_school_year_selected.data('start-month'),
		start_year = $timesheet_school_year_selected.data('start-year'),
		end_month = $timesheet_school_year_selected.data('end-month'),
		end_year = $timesheet_school_year_selected.data('end-year'),
		schools = $timesheet_school_year_selected.data('schools'),
		current_langauge = $('#active-language').text(),
		$select = $('<select></select>', {
			'id':'school-dropdown',
			'class':'form-control',
			'name':'school'
		});

	if (schools.length > 0) {
		$select.append($('<option></option>', {
			'value':'0',
			'text':'All Schools'
		}));
		
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
			'text':'No schools available. Please add a school from the School Years tab.'
		}));
		$select.attr('disabled', 'true');
		$('.btn-generate-pdf').attr('disabled', 'true')
	}
	
	$timesheet_school_dropdown_cell.html($select);
	TIMESHEET.populateCalendarDropdownValues(e, $timesheet_start_month_dropdown_cell, 'start-date', start_month, end_month, start_year, end_year);
	TIMESHEET.populateMonthToValues();
};

TIMESHEET.populateMonthToValues = function(e) {
	var $timesheet_school_year_selected = $('#timesheet-school-year').find(':selected'),
		$timesheet_start_month_dropdown_cell = $('#timesheet-start-month-dropdown-cell'),
		$timesheet_end_month_dropdown_cell = $('#timesheet-end-month-dropdown-cell'),
		selected_start_month_value_array = $timesheet_start_month_dropdown_cell.find(':selected').val().split('-'),
		start_year = parseInt(selected_start_month_value_array[0]),
		start_month = parseInt(selected_start_month_value_array[1]),
		end_month = $timesheet_school_year_selected.data('end-month'),
		end_year = $timesheet_school_year_selected.data('end-year');

	TIMESHEET.populateCalendarDropdownValues(e, $timesheet_end_month_dropdown_cell, 'end-date', start_month, end_month, start_year, end_year);
};

TIMESHEET.updateHiddenInputField = function(e) {
	var $element = $(e.target);
	$element.parent().parent().parent().find('input').attr('value', $('#editable-field').val());
};

$(document).ready(function(){
	TIMESHEET.populateDropdownValues();
	
	$(document)
		.on('change', '#timesheet-school-year', TIMESHEET.populateDropdownValues)
		.on('change', '#timesheet-start-month-dropdown-cell select', TIMESHEET.populateMonthToValues);
	
	$('.editable-label').each(function() {
		$(this).on('change', TIMESHEET.updateHiddenInputField);
	});
});