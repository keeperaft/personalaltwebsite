var SCHOOL_PERIODS = SCHOOL_PERIODS || {};

SCHOOL_PERIODS.populateDropdownValues = function() {
	var $timesheet_school_year_selected = $('#school-periods-school-year').find(':selected'),
		$timesheet_school_dropdown_cell = $('#school-periods-school-dropdown-cell'),
		selected_id = $timesheet_school_dropdown_cell.data('selected-id'),
		start_month = $timesheet_school_year_selected.data('start-month'),
		start_year = $timesheet_school_year_selected.data('start-year'),
		end_month = $timesheet_school_year_selected.data('end-month'),
		end_year = $timesheet_school_year_selected.data('end-year'),
		schools = $timesheet_school_year_selected.data('schools');

	$timesheet_school_dropdown_cell.html(BASE.generateSchoolDropdown(schools, selected_id));
	SCHOOL_PERIODS.changeSchoolHref();
};

SCHOOL_PERIODS.addNewTimePeriod = function(e) {
	var $this = $(e.target),
		$entry_row = $this.parent().parent(),
		$table = $entry_row.parent(),
		$period_number_element = $table.find('.input-period-number'),
		$start_time_input = $table.find('.start-time'),
		$end_time_input = $table.find('.end-time'),
		period_type_id = $this.data('period-type-id'),
		start_time = $start_time_input.val(),
		end_time = $end_time_input.val(),
		period_number = $period_number_element.html(),
		post_url = $this.data('url');

	if (!BASE.validateTimeHhMm(start_time) || !BASE.validateTimeHhMm(end_time)) {
		BASE.showNotification(NOTIFICATION_FAILURE, $('.incorrect-format-wrapper').text());
		return;
	}

	// The end time must be later than the start time.
	var start_time_array = start_time.split(':'),
		end_time_array = end_time.split(':'),
		start_time_hour = parseInt(start_time_array[0]),
		start_time_minute = parseInt(start_time_array[1]),
		end_time_hour = parseInt(end_time_array[0]),
		end_time_minute = parseInt(end_time_array[1]),
		is_hour_incorrect = start_time_hour > end_time_hour,
		is_minute_incorrect = start_time_hour == end_time_hour && start_time_minute > end_time_minute;

	if (is_hour_incorrect || is_minute_incorrect) {
		BASE.showNotification(NOTIFICATION_FAILURE, $('.earlier-end-time-wrapper').text());
		return;
	}

	// 5:00 --> 05:00
	start_time = BASE.addLeadingZero(start_time_hour)+':'+BASE.addLeadingZero(start_time_minute);
	end_time = BASE.addLeadingZero(end_time_hour)+':'+BASE.addLeadingZero(end_time_minute);

	$.ajax({
		url: post_url,
		method: "POST",
		data: {
			'period_type_id': period_type_id,
			'period_number': period_number,
			'start_time': start_time,
			'end_time': end_time
		},
		success: function(msg){
			if (msg.is_success == true) {
				var period_id = msg.messages.period_id,
					$new_row = $('<tr></tr>', {
						'data-id': period_id,
						'data-update-period-number-url': '/schedules/update_period_number'
					}),
					$span_period = $('<span></span>', {'class': 'period-number', 'html': period_number}),
					$span_editable_text_start_time = $('<span></span>', {
						'class': 'editable-label',
						'data-url': '/schedules/update_period_start_time',
						'data-id': period_id,
						'data-value': start_time,
						'data-type': 'textfield'
					}),
					$span_editable_text_end_time = $('<span></span>', {
						'class': 'editable-label',
						'data-url': '/schedules/update_period_end_time',
						'data-id': period_id,
						'data-value': end_time,
						'data-type': 'textfield'
					}),
					$delete_button = $('<button></button>', {
						'type': 'button"',
						'class': 'btn btn-tertiary delete-time-period-button',
						'data-id': period_id,
						'data-url': '/schedules/delete_period',
					}),
					$glyphicon_trash = $('<span></span>', {
						'class': 'glyphicon glyphicon-trash'
					})
					$cell_period_number = $('<td></td>', {}),
					$cell_start_time = $('<td></td>', {}),
					$cell_end_time = $('<td></td>', {}),
					$cell_actions = $('<td></td>', {});

				$span_editable_text_start_time.append(start_time);
				$span_editable_text_end_time.append(end_time);

				$delete_button.append($glyphicon_trash);
				$delete_button.append($('.delete-time-period-wrapper').text());

				$cell_period_number.append($span_period);
				$cell_start_time.append($span_editable_text_start_time);
				$cell_end_time.append($span_editable_text_end_time);
				$cell_actions.append($delete_button);

				$new_row.append($cell_period_number);
				$new_row.append($cell_start_time);
				$new_row.append($cell_end_time);
				$new_row.append($cell_actions);
				$new_row.insertBefore($entry_row);

				$start_time_input.val('');
				$end_time_input.val('');
				$period_number_element.html(parseInt(period_number)+1);

				BASE.showNotification(NOTIFICATION_SUCCESS, $('.new-time-period-wrapper').text());
			}
			else {
				BASE.showNotification(NOTIFICATION_FAILURE, msg.messages);
			}	
		},
		error: function(msg){
			BASE.showNotification(NOTIFICATION_FAILURE, 'A server error has occured. Please try again later.');
		}
	});
};

SCHOOL_PERIODS.prepareLastPeriodNumber = function() {
	$('.input-period-number').each(function() {
		var $this = $(this),
			$parent_table = $this.parent().parent().parent(),
			$span_last_period = $parent_table.find('.period-number').last(),
			last_period_number = parseInt($span_last_period.html());

		if(isNaN(last_period_number)) {
			last_period_number = 1;
		}
		else {
			last_period_number += 1;
		}
		$this.html(last_period_number);
	});
};

SCHOOL_PERIODS.changeSchoolHref = function() {
	var school_id = $('#school-periods-school-dropdown-cell select').find(':selected').val(),
		href = '/schedules/school_periods/'+school_id,
		$link = $('#view-school-profile-button');

	$link.attr('href', href);
}

SCHOOL_PERIODS.shiftPeriodNumberBackwardsByOneUntilInput = function($row) {
	var $row_after = $row.next(),
		$period_number_element = $row_after.find('.period-number'),
		$input_period_number_element = $row_after.find('.input-period-number'),
		period_id = $row_after.data('id'),
		post_url = $row_after.data('update-period-number-url'),
		period_number = parseInt($period_number_element.html()),
		input_period_number = parseInt($input_period_number_element.html());

	if (isNaN(input_period_number) && !isNaN(period_number)) {
		period_number -= 1;
		$period_number_element.html(period_number);

		$.ajax({
			url: post_url,
			method: "POST",
			data: {'id': period_id, 'value':period_number},
			success: function(msg){
				SCHOOL_PERIODS.shiftPeriodNumberBackwardsByOneUntilInput($row_after);
			},
			error: function(msg){
				BASE.showNotification(NOTIFICATION_FAILURE, 'A server error has occured. Please try again later.');
			}
		});
	}
	else if(isNaN(period_number) && !isNaN(input_period_number)) {
		input_period_number -= 1;
		$input_period_number_element.html(input_period_number);
	}
}

SCHOOL_PERIODS.deleteCurrentRow = function(e) {
	var $this = $(e.target),
		$row_to_delete = $this.parent().parent(),
		period_id = $this.data('id'),
		post_url = $this.data('url');

	$.ajax({
		url: post_url,
		method: "POST",
		data: {'id': period_id},
		success: function(msg){
			$row_to_delete.hide(500, function() {
				$row_to_delete.remove();
			});
			SCHOOL_PERIODS.shiftPeriodNumberBackwardsByOneUntilInput($row_to_delete);
			BASE.showNotification(NOTIFICATION_SUCCESS, 'The period deletion was successful.');
		},
		error: function(msg){
			BASE.showNotification(NOTIFICATION_FAILURE, 'A server error has occured. Please try again later.');
		}
	});


		
}

$(document).ready(function(){
	SCHOOL_PERIODS.populateDropdownValues();
	SCHOOL_PERIODS.prepareLastPeriodNumber();
	SCHOOL_PERIODS.changeSchoolHref();

	$(document)
		.on('change', '#school-periods-school-year', SCHOOL_PERIODS.populateDropdownValues)
		.on('change', '#school-periods-school-dropdown-cell > select', SCHOOL_PERIODS.changeSchoolHref)
		.on('click', '.btn-add-new-time-period', SCHOOL_PERIODS.addNewTimePeriod)
		.on('click', '.delete-time-period-button', SCHOOL_PERIODS.deleteCurrentRow);
});