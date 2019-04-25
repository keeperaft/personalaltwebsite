var CHECK_REIMBURSEMENTS = CHECK_REIMBURSEMENTS || {};

CHECK_REIMBURSEMENTS.calculateTotalCost = function() {
	var total_cost = 0;
	$('.individual-reimbursement-cost').each(function(){
		var cost = parseInt($(this).html());
		total_cost += cost;
	});
	$('.total-reimbursement-cost').html(total_cost);
};

CHECK_REIMBURSEMENTS.toggleReimbursementEntry = function(e) {
	var $this = $(e.target),
		$row = $this.parent().parent().parent().parent(),
		is_included = $this.bootstrapSwitch('state');

	if (is_included) {
		$row.find('.reimbursement-date-cancelled').attr('class', 'reimbursement-date');
		$row.find('.route-info-cancelled').attr('class', 'route-info');
		$row.find('.individual-reimbursement-cost-cancelled').attr('class', 'individual-reimbursement-cost');
		$row.find('.round-trip-marker-cancelled').attr('class', 'round-trip-marker');
	}
	else {
		$row.find('.reimbursement-date').attr('class', 'reimbursement-date-cancelled');
		$row.find('.route-info').attr('class', 'route-info-cancelled');
		$row.find('.individual-reimbursement-cost').attr('class', 'individual-reimbursement-cost-cancelled');
		$row.find('.round-trip-marker').attr('class', 'round-trip-marker-cancelled');
	}
	CHECK_REIMBURSEMENTS.calculateTotalCost()
}

CHECK_REIMBURSEMENTS.windowScroll = function() {
    // Get current scroll position
    var scroll_pixels_from_top = $(window).scrollTop(),
        $reimbursement_header_row = $('.reimbursement-header-row'),
        scroll_to_top_pixels = 300;

    if (scroll_pixels_from_top >= scroll_to_top_pixels) {
        $reimbursement_header_row.css('position', 'sticky');
        $reimbursement_header_row.css('top', '0px');
        $reimbursement_header_row.css('background-color', '#FFF');
        $reimbursement_header_row.css('border-radius', '0 0 5px 5px');
        $reimbursement_header_row.css('z-index', '2');
        $reimbursement_header_row.css('box-shadow', '-2px 4px 5px #AAA');
        $reimbursement_header_row.addClass('container');
        $reimbursement_header_row.addClass('reimbursement-header-container');
    }
    else {
        $reimbursement_header_row.removeClass('container');
        $reimbursement_header_row.removeClass('reimbursement-header-container');
        $reimbursement_header_row.css('position', 'relative');
        $reimbursement_header_row.css('top', 'auto');
        $reimbursement_header_row.css('background-color', 'auto');
        $reimbursement_header_row.css('border-radius', '0px');
        $reimbursement_header_row.css('z-index', '0');
        $reimbursement_header_row.css('box-shadow', 'none');
     }
};

CHECK_REIMBURSEMENTS.generateScript = function() {
	var script = '',
		all_routes = {},
		$raw_code_available = $('.raw-code-variable'),
		$code_area = $('.raw-code-constant > .all-routes'),
		$btn_copy = $('.btn-copy');

	$code_area.html('');
	$btn_copy.removeAttr('disabled');
	$btn_copy.text('Copy');

	$('.route-info').each(function() {
		var $this = $(this),
			id = $this.data('route-id');

		if (all_routes.hasOwnProperty(id) == false) {
			all_routes[id] = {
				'dates': [],
				'destination': $this.data('destination'),
				'from': $this.data('from'),
				'to': $this.data('to'),
				'method': $this.data('method'),
				'isRoundTrip': $this.data('isRoundTrip'),
				'fee': $this.data('total-cost'),
				'index': $this.data('index'),
			}
		}
		all_routes[id].dates.push($this.data('day'));		
	});

	for (key in all_routes) {
		var route = all_routes[key],
			dates = route['dates'],
			destination = route['destination'],
			from = route['from'],
			to = route['to'],
			method = route['method'],
			is_round_trip = route['isRoundTrip'],
			fee = route['fee'],
			dates_content = ['['],
			index = route['index'];

		if (is_round_trip == 'True') {
			is_round_trip = 'true';
		}
		else {
			is_round_trip = 'false'
		}

		for (var i=0; i<dates.length; i++) {
			dates_content.push(BASE.getSingleQuotedText(dates[i]));
			if (i < dates.length - 1) {
				dates_content.push(',');
			}
		}
		dates_content.push(']');

		$raw_code_available.find('.date-array').html(dates_content.join(''));
		$raw_code_available.find('.destination').html(BASE.getSingleQuotedText(destination));
		$raw_code_available.find('.from').html(BASE.getSingleQuotedText(from));
		$raw_code_available.find('.to').html(BASE.getSingleQuotedText(to));
		$raw_code_available.find('.method').html(BASE.getSingleQuotedText(method));
		$raw_code_available.find('.is-round-trip').html(is_round_trip);
		$raw_code_available.find('.fee').html(fee);

		$code_area.append($raw_code_available.text())
	}

	$('#reimbursement-code-generated-script').html($('.raw-code-constant').text());
};

CHECK_REIMBURSEMENTS.addNewRoute = function() {
	// Get the values for calendar and route information
	var $reimbursement_entry = $('#reimbursement-entry-input'),
		$reimbursement_entry_select = $('#add-reimbursement-route'),
		$reimbursement_entry_input = $('#add-reimbursement-date'),
		$selected_route = $reimbursement_entry.find('#add-reimbursement-route').find(':selected'),
		expected_year = $reimbursement_entry.data('year'),
		expected_month = $reimbursement_entry.data('month'),
		date = $reimbursement_entry.find('#add-reimbursement-date').val().trim(),
		route_id = $selected_route.data('route-id'),
		destination = $selected_route.data('destination'),
		index = $selected_route.data('index'),
		from = $selected_route.data('from'),
		to = $selected_route.data('to'),
		method = $selected_route.data('method'),
		is_round_trip = $selected_route.data('is-round-trip') == 'True' ? true : false,
		total_cost = $selected_route.data('total-cost'),
		date_array = date.split('-'),
		year = date_array[0],
		month = date_array[1],
		day = date_array[2];

	// Check if calendar is empty, if it is, show an error notification and return
	if (date == '') {
		BASE.showNotification(NOTIFICATION_FAILURE, "Reimbursement date must be filled.");
		return;
	}

	// Check if the calendar's month and year is the same as the current month and year
	if (year != expected_year || month != expected_month) {
		BASE.showNotification(NOTIFICATION_FAILURE, "The year and month must be the same as the year and month of reimbursement.");
		return;
	}

	// If not, reset the fields
	$reimbursement_entry_input.val('');
	$reimbursement_entry_select.val($reimbursement_entry_select.find('option:first').val());

	// Use the retrieved values to add a new row
	var $new_row = $('<tr></tr>', {}),
		$cell_checkbox = $('<td></td>', {}),
		$cell_reimbursement_date = $('<td></td>', {
			'class': 'reimbursement-date',
			'html': date
		}),
		$cell_route_info = $('<td></td>', {
			'class': 'route-info',
			'data-day': day,
			'data-route-id': route_id,
			'data-destination': destination,
			'data-from': from,
			'data-to': to,
			'data-index': index,
			'data-method': method,
			'data-is-round-trip': is_round_trip,
			'data-total-cost': total_cost,
			'html': destination
		}),
		$cell_cost = $('<td></td>', {}),
		$toggle_switch = $('<input/>', {
			'type': 'checkbox',
			'class': 'toggle-switch include-switch',
			'checked': 'true',
			'data-on-text': 'Yes',
			'data-off-text': 'No',
			'data-on-color': 'success'
		}),
		$reimbursement_cost_span = $('<span></span>', {
			'class': 'individual-reimbursement-cost',
			'html': total_cost
		}),
		$round_trip_marker = $('<span></span>', {
			'class': 'round-trip-marker',
			'html': 'Round Trip'
		});

	// $toggle_switch.bootstrapSwitch();
	$cell_checkbox.html($toggle_switch);
	$cell_cost.html($reimbursement_cost_span)

	if (is_round_trip) {
		$cell_cost.append(' ');
		$cell_cost.append($round_trip_marker);
	}

	$new_row.html($cell_checkbox);
	$new_row.append($cell_reimbursement_date);
	$new_row.append($cell_route_info);
	$new_row.append($cell_cost);
	$new_row.insertBefore($reimbursement_entry);
	$('.include-switch').bootstrapSwitch();

	// Recalculate the total cost
	CHECK_REIMBURSEMENTS.calculateTotalCost();

	// Set the should_display_confirmation_message flag to true
};

CHECK_REIMBURSEMENTS.prepareDatePicker = function(e) {
	var $this = $(e.target),
		year = $this.data('year'),
		month = $this.data('month'),
		count_days = BASE.dayCount(month, year);

	$this.datepicker({ 
		format: 'yyyy-mm-dd',
		startDate: year+'-'+month+'-01',
		endDate: year+'-'+month+'-'+count_days,
	});
};

CHECK_REIMBURSEMENTS.prepareDatePickerPlaceholder = function() {
	var $element = $('#add-reimbursement-date');
	$element.attr('placeholder', $element.data('year')+'-'+BASE.addLeadingZero($element.data('month'))+'-12');
};

CHECK_REIMBURSEMENTS.scrollToAddItem = function() {
	$('html, body').animate({ scrollTop: $("#reimbursement-entry-input").offset().top }, 500);
	$('#add-reimbursement-date').focus();
};

$(document).ready(function(){
	CHECK_REIMBURSEMENTS.calculateTotalCost();
	CHECK_REIMBURSEMENTS.prepareDatePickerPlaceholder();

	$(window)
        .scroll(CHECK_REIMBURSEMENTS.windowScroll)

	$(document)
		.on('switchChange.bootstrapSwitch', '.include-switch', CHECK_REIMBURSEMENTS.toggleReimbursementEntry)
		.on('click', '#reimbursement-code-generation-button', CHECK_REIMBURSEMENTS.generateScript)
		.on('click', '#add-new-route', CHECK_REIMBURSEMENTS.addNewRoute)
		.on('click', '#add-reimbursement-entry-button', CHECK_REIMBURSEMENTS.scrollToAddItem)
		.on('focus', '#add-reimbursement-date', CHECK_REIMBURSEMENTS.prepareDatePicker);
});