var BASE = BASE || {};

var NOTIFICATION_SUCCESS = 0,
	NOTIFICATION_FAILURE = 1,
	KEY_ENTER = 13, // Enter key
	KEY_ESC = 27; // Escape key

BASE.closeDemoInfo = function(){
	$.ajax({
		url: '/remove_demo_info',
		method: "POST",
		success: function(msg){},
		error: function(msg){
			console.log('Failure upon removing the demo information modal.');
		}
	});
}

BASE.getLocalizedMonthList = function() {
	return [
		$('#string-january').text(),
		$('#string-february').text(),
		$('#string-march').text(),
		$('#string-april').text(),
		$('#string-may').text(),
		$('#string-june').text(),
		$('#string-july').text(),
		$('#string-august').text(),
		$('#string-september').text(),
		$('#string-october').text(),
		$('#string-november').text(),
		$('#string-december').text(),
	]
}

BASE.generateSchoolDropdown = function(schools, selected_id) {
	var $select = $('<select></select>', {
			'class':'form-control',
			'name':'school',
			'id':'select_school'
		}),
		current_langauge = $('#active-language').text();

	if (schools.length > 0) {		
		// Populate dropdown for schools
		for(var item in schools) {
			var school_name = '';
			if (current_langauge == 'ja') {
				school_name = schools[item].name_kanji
			}
			else {
				school_name = schools[item].name
			}
			var id = schools[item].id,
				$option = $('<option></option>', {
					'value': id,
					'text':school_name
				});
			if (selected_id == id) {
				$option.attr('selected', 'selected');
			}
			$select.append($option);
		}
	}
	else {
		$select.append($('<option></option>', {
			'value':'0',
			'text':'No schools available. Please add a school from the School Years tab.'
		}));
		$select.attr('disabled', 'true');
	}
	return $select;
};

BASE.generateYearMonthDropdown = function(start_year, end_year, start_month, end_month) {
	var month_list = BASE.getLocalizedMonthList(),
		month_count = BASE.getMonthCount(start_year, end_year, start_month, end_month),						
		$select = $('<select></select>', {
			'class':'form-control',
			'name':'month'
		});

	for(var i=0; i<month_count; i++) {
		var month_index = start_month + i - 1,
			name_year = start_year + Math.floor(month_index/12),
			month_index_mod_12 = month_index%12,
			name_month = month_list[month_index_mod_12],
			value = name_year+'-'+((month_index_mod_12)+1),
			name_month_year = name_month+' '+name_year,
			date = new Date(),
			current_year = date.getFullYear(),
			current_month = date.getMonth(),
			$option = $('<option></option>', {
				'value':value,
				'text':name_month_year
			});

		if (current_year == name_year && current_month == month_index_mod_12) {
			$option.attr('selected', 'selected');

		}
		$select.append($option);
	}
	return $select;
};

BASE.removeDashedOption = function() {
	$('.remove-dash-select').each(function() {
		var $potential_dashed_option = $(this).find('option:first-child');
		if ($potential_dashed_option.html() == '---------') {
			$potential_dashed_option.remove();
		}
	});
};

BASE.ajaxButtonClick = function(e) {
	var $this = $(e.target),
		post_url = $this.data('url');
	$.ajax({
		url: post_url,
		method: "POST",
		success: function(msg){
			location.reload();
		},
		error: function(msg){
			console.log('AJAX modal form validation failure. The URL used was: '+ post_url);
		}
	});
};

// Obviously not my code lol
BASE.alphabeticallyArrangeOptions = function(options) {
	var arr = options.map(function(_, o) {
		return { t: $(o).text(), v: o.value, s: $(o).attr('selected'), d: $(o).attr('data-lessons') };}).get();
	arr.sort(function(o1, o2) { return o1.t > o2.t ? 1 : o1.t < o2.t ? -1 : 0; });
	options.each(function(i, o) {
		if (arr[i].s) {
			$(o).attr('selected', 'selected');
		}
		else {
			$(o).removeAttr('selected');
		}
		o.value = arr[i].v;
		$(o).text(arr[i].t);
		$(o).attr('data-lessons', arr[i].d) 
	});
};

BASE.setBackgroundColor = function() {
	$('.set-data-color').each(function() {
		var $this = $(this);
		$this.css('background-color', $this.data('color'))
	});
};

BASE.setTextColor = function() {
	$('.set-text-color').each(function() {
		var $this = $(this);
		$this.css('color', $this.data('color'))
	});
};

BASE.validateTimeHhMm = function(input) {
	return /^([0-1]?[0-9]|2[0-4]):([0-5][0-9])(:[0-5][0-9])?$/.test(input);
};

BASE.getMonthCount = function(start_year, end_year, start_month, end_month) {
	return (13 - start_month) + (end_year - start_year - 1)*12 + end_month;
};

BASE.removeLeadingTrailingZeros = function() {
	$('.parse-int').each(function() {
		var $this = $(this);
		$this.html(parseInt($this.html()));
	});
}

BASE.getSingleQuotedText = function(input) {
	var output = ["'"];
	output.push(input);
	output.push("'");
	return output.join('');
}

BASE.addLeadingZero = function(input) {
	input = input+"";
	while(input.length < 2) {
		input = "0"+input;
	}
	return input;
};
BASE.registerCustomTag = function(new_tag_name, custom_function, is_element_replacement) {
	document.createElement(new_tag_name);
	
	var tag_instances = document.getElementsByTagName(new_tag_name);
	var tag_count = tag_instances.length;

	for(var i=0; i<tag_count; i++) {
		custom_function(tag_instances[0]);
	}
};
BASE.removeMe = function() {
	$('.remove-me').each(function() {
		$(this).replaceWith($(this).html());
	});
};
BASE.csrfSafeMethod = function(method) { 
	// These HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method)); 
};
BASE.csrfToken = function() {
	// All AJAX post requests sent must have a CSRF token as a request header
	var csrf_token = Cookies.get('csrftoken');
	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if (!BASE.csrfSafeMethod(settings.type) && !this.crossDomain) {
				xhr.setRequestHeader("X-CSRFToken", csrf_token);
			}
		}
	});
};
BASE.editableDropdown = function() {
	// Display the correct value for editable-dropdowns
	$('.editable-dropdown').each(function() {
		var $this = $(this);
		var dropdown_values = $this.data('dropdown-values');
		$this.html(dropdown_values[$this.data('value')]);
	});
};
BASE.submitModalForm = function(event) {
	var $this = $(event.target);
	if ($this.attr('enctype') != 'multipart/form-data') {
		event.preventDefault();
		var $this = $(event.target),
			$modal_button = $('.modal.fade.in > .modal-dialog > .modal-content > .modal-form > .modal-footer > .btn-primary'),
			post_url = $this.attr('action'),
			data = $this.serialize(),
			loading_text = $('#string-loading').text();

		$modal_button.html(loading_text);
		$modal_button.attr('disabled', 'disabled');
		$modal_button.attr('class', 'btn btn-disabled');

		$.ajax({
			url: post_url,
			method: "POST",
			data: data,
			success: function(msg){
				// If the validation is successful, refresh the page and display the success message.
				if (msg.is_success === true) {
					location.reload();
				}
				// Else, display whatever errors there are within the modal
				else {
					var $error_message = $('<div></div>', {
						'class': 'alert modal-alert alert-danger alert-dismissable'
						}),
						$unordered_list = $('<ul></ul>', {}),
						$close_button = $('<a></a>', {
							'href': '#',
							'class': 'close',
							'data-dismiss': 'alert',
							'aria-label': 'close',
							'html': '&times;'
						});

					for(var key in msg.messages) {
						var key_proper_case = BASE.toTitleCase(key.replace(/_/g, ' '));
						$unordered_list.append($('<li></li>', {
							'text': key_proper_case+': '+msg.messages[key]
						}));
					}
					$modal_button.html($('#string-save').text());
					$modal_button.removeAttr('disabled');
					$modal_button.attr('class', 'btn btn-primary');
					$error_message.append($close_button);
					$error_message.append($unordered_list);
					$('.modal.fade.in .modal-messages').append($error_message);
				}
				
			},
			error: function(msg){
				console.log('AJAX modal form validation failure. The URL used was: '+ post_url+', and the message was: '+msg.responseText);
			}
		});
	}
};
BASE.setEditableLabels = function(e) {
	$('.editable-label').each(function() {
		var $this = $(this);
		if ($this.html().trim() == '') {
			$this.html('N/A');
		}
	});
};
BASE.turnLabelIntoField = function(e) {
	var $label_editing = $('.label-editing'),
		$this = $(e.target),
		old_classes = $this.attr('class'),
		value = $this.data('value'),
		editable_type = $this.data('type');

	// Users cannot click on another editable label while another label is actively being edited
	if ($label_editing.length) {
		return;
	}
	
	$this.attr('class', 'label-editing');
	$this.data('old-value', value);

	var $input_group = $('<div></div>', {
		'class': 'input-group'
	}),
		$input_type = null;

	// Build the editable field
	if (editable_type == 'numeric-textfield') {
		$input_type = $('<input/>', {
			'type': 'number',
			'id': 'editable-field',
			'class': 'form-control col-xs-10',
			'data-old-class': old_classes,
			'value': value
		});
	}
	else if (editable_type == 'textarea') {
		$input_type = $('<textarea></textarea>', {
			'id': 'editable-field',
			'data-old-class': old_classes,
			'value': value
		});
	}
	else if (editable_type == 'dropdown') {
		var dropdown_values = $this.data('dropdown-values');
		$input_type = $('<select></select>', {
			'class': 'form-control',
			'data-old-class': old_classes,
			'id': 'editable-field'
		});
		for(var key in dropdown_values) {
			var $option = $('<option></option>', {
				'value': key,
				'text': dropdown_values[key],
			});
			if (key == value) {
				$option.attr('selected', 'selected');
			}
			$input_type.append($option);
		}
	}
	else {
		// Text field
		$input_type = $('<input/>', {
			'type': 'text',
			'id': 'editable-field',
			'class': 'form-control col-xs-10',
			'data-old-class': old_classes,
			'value': value
		});
	}

	// Done button
	$input_group.append($input_type);
	$input_group.append(BASE.constructEditableActions(false));
	$('#editable-overlay').css('display', 'block');

	// Replace the inner HTML
	$this.html($input_group);
	$('#editable-field').focus();
};
BASE.constructEditableActions = function(is_loading) {
	var $editable_actions = $('<div></div>', {
		'class': 'input-group-btn',
		'id': 'editable-field-actions'
	});
	if (is_loading) {
		$editable_actions.append($('<button></button>', {
			'id': 'loading-icon',
			'type': 'button',
			'class': 'btn btn-disabled',
			'html': '<span class="glyphicon glyphicon-hourglass"></span>'
		}));
	}
	else {
		$editable_actions.append($('<button></button>', {
			'type': 'button',
			'id': 'cancel-button',
			'class': 'btn btn-cancel',
			'html': '<span class="glyphicon glyphicon-minus-sign"></span>'
		}));
		$editable_actions.append($('<button></button>', {
			'type': 'button',
			'id': 'done-button',
			'class': 'btn btn-success',
			'html': '<span class="glyphicon glyphicon-ok"></span>'
		}));
	}
	return $editable_actions;
};

BASE.editableOverlayClick = function() {
	$('#cancel-button').click();
};

BASE.saveNewValueOfEditableField = function($this) {
	// this-element -> form-control -> target-parent
	var $editable_field = $('#editable-field'),
		old_classes = $editable_field.data('old-class'),
		parent_element = $this.parent().parent().parent(),
		value = $editable_field.val(),
		id = parent_element.data('id'),
		post_url = parent_element.data('url');

	// is_editable = False? Disables the input field and shows a loading icon
	// is_editable = True? Enables the input field and shows the OK/CANCEL icons
	function toggleEditableField(is_editable) {
		// Warning: This method will fail if BASE.return_editable_field() has been called beforehand
		// because there won't be any "#editable-field" or "#done-button" around anymore
		$editable_field.attr('disabled', 'disabled');

		if (is_editable) {
			$editable_field.removeAttr('disabled');
		}

		$('#editable-field-actions').html(BASE.constructEditableActions(!is_editable));
	}

	toggleEditableField(false);

	if (post_url !== '') {
		$.ajax({
			url: post_url,
			method: "POST",
			data: {
				'id': id,
				'value': value 
			},
			success: function(msg){
				// If the validation is successful, re-enable the field
				if (msg.is_success === true) {
					BASE.return_editable_field(parent_element, value, old_classes);
				}
				// Else, display whatever errors there are within the modal
				else {
					toggleEditableField(true);
					console.log('An error has occured while saving in the database. Here is the message: '+msg);
				}
			},
			error: function(msg){
				console.log('AJAX modal form validation failure. The URL used was: '+ post_url);
			}
		}); 
	}
};
BASE.returnEditableFieldToPreviousState = function($this) {
	// this-element -> form-control -> target-parent
	var parent_element = $this.parent().parent().parent(), 
		$editable_field = $('#editable-field'),
		old_classes = $editable_field.data('old-class'),
		value = parent_element.data('old-value');
	BASE.return_editable_field(parent_element, value, old_classes);
	$('#editable-overlay').css('display', 'none');
};
BASE.editableFieldKeyDownCheck = function(event) {
	var code = event.keyCode || event.which;
	if (code == KEY_ENTER) {
		$('#done-button').click();
	}
	else if (code == KEY_ESC) {
		$('#cancel-button').click();
	}
};
BASE.saveNewValueOfToggledSwitch = function($element, event, state) {
	var post_url = $element.data('url');

	if(post_url !== undefined) {
		var id = $element.data('id');
		$.ajax({
			url: post_url,
			method: "POST",
			data: {
				'id': id,
				'value': state 
			},
			success: function(msg){
				// Show success notification
				BASE.showNotification(NOTIFICATION_SUCCESS, msg.messages);
			},
			error: function(msg){
				// Show error notification
				BASE.showNotification(NOTIFICATION_FAILURE, msg.messages);
			}
		});
	}
};
BASE.checkScrollDependentElements = function() {
	// Get current scroll position
	var scroll_pixels_from_top = $(window).scrollTop(),
		$scroll_to_top = $('#scroll-to-top'),
		scroll_to_top_pixels = 200;

	// Scroll to top
	if (scroll_pixels_from_top >= scroll_to_top_pixels) {
		// Show "Scroll to Top" button
		$scroll_to_top.show();
	}
	else {
		// Hide "Scroll to Top" button
		$scroll_to_top.hide();
	}
};
BASE.scrollToTop = function() {
	$('html, body').animate({ scrollTop: 0 }, 500);
	return false;
};
BASE.changeLanguage = function(e) {
	// Get the target language
	var $this = $(e.target),    
		new_language = $this.data('language'),
		post_url = $this.data('url') + new_language + '/';

	// Switch language via ajax
	$.ajax({
		url: post_url,
		method: "POST",
		data: {},
		success: function(msg){
			// Refresh the current page when the language switch is successful
			location.reload();
		},
		error: function(msg){
			console.log('Language change failed. The URL used was: '+ post_url+', and the message was '+msg.responseText);
			// location.reload();
		}
	});
};
BASE.toggleVisibility = function(e) {
	var $this = $(e.target),
		string_show = $('#string-show').html(),
		string_hide = $('#string-hide').html(),
		current_string = $this.html().trim(),
		target = $this.data('target');

	$(target).toggle();

	if (current_string == string_show) {
		$this.html(string_hide);
	}
	else {
		$this.html(string_show);
	}
};
BASE.copyText = function(e) {
	var $this = $(e.target);
	$this.text($this.data('after-click-text'));
	$this.attr('disabled', 'true');
};
BASE.showNotification = function(notification_type, message) {
	var alert_type = 'alert-success';

	if (notification_type == NOTIFICATION_FAILURE) {
		alert_type = 'alert-danger';
	}

	var selector_message = [];
	selector_message.push('.fixed-alerts ');
	selector_message.push('.');
	selector_message.push(alert_type);

	var selector_target = selector_message.join('');
	selector_message.push(' .fixed-alert-message');

	$(selector_message.join('')).html(message);

	$(selector_target).css('display', 'block');
	$('.fixed-alerts-row').append($(selector_target).clone().fadeOut(5000));
};
BASE.return_editable_field = function(parent_element, value, old_classes) {
	// Returns input fields into editable labels
	var $parent = $(parent_element);
	$parent.data('value', value);

	if ($parent.data('type') == 'dropdown') {
		var dropdown_values = $parent.data('dropdown-values');
		value = dropdown_values[value];
	}

	if (value === '') {
		value = 'N/A';
	}

	$('#editable-overlay').css('display', 'none');
	$parent.attr('class', old_classes);
	$parent.html(value);
};
BASE.toTitleCase = function(str){
	return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
};
BASE.dayCount = function(input_month, input_year) {
	// 1 means January for input_month
	return new Date(input_year, input_month, 0).getDate();
};
BASE.rgbTohex = function(rgb) {
	rgb = rgb.match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/);
	function hex(x) {
		return ("0" + parseInt(x).toString(16)).slice(-2);
	}
	return ("#" + hex(rgb[1]) + hex(rgb[2]) + hex(rgb[3])).toUpperCase();
};

// Registered modal functions
BASE.modalContent = function(element) {
	var $element = $(element),
		modal_id = $element.attr('id'),
		$modal_fade = $('<div></div>', {
			'class': 'modal fade',
			'id': modal_id,
			'tabindex': '-1',
			'role': 'dialog'
		}),
		$modal_dialog = $('<div></div>', {
			'class': 'modal-dialog'
		}),
		$modal_content = $('<div></div>', {
			'class': 'modal-content',
			'html': $element.html()
		});
	
	$modal_dialog.append($modal_content);
	$modal_fade.append($modal_dialog);
	$element.replaceWith($modal_fade);
};

BASE.modalHead = function(element) {
	var $element = $(element),
		$modal_header = $('<div></div>', {
			'class': 'modal-header'
		}),
		$button_close = $('<button></button>', {
			'type': 'button',
			'class': 'close',
			'data-dismiss': 'modal',
			'html': '&times;'
		}),
		$h4 = $('<h4></h4>', {
			'id': 'form-modal-title',
			'class': 'modal-title',
			'html': $element.html()
		});

	$modal_header.append($button_close);
	$modal_header.append($h4);
	$element.replaceWith($modal_header);
};

BASE.modalBody = function(element) {
	var $element = $(element),
		$modal_body = $('<div></div>', {
			'class': 'modal-body'
		}),
		$modal_messages = $('<div></div>', {
			'class': 'modal-messages'
		});

	$modal_body.append($modal_messages);
	$modal_body.append($element.html());
	$element.replaceWith($modal_body);
};

BASE.modalFooter = function(element) {
	var $element = $(element),
		close_text = $('#string-close').text(),
		save_text = $('#string-save').text(),
		$modal_footer = $('<div></div>', {
			'class': 'modal-footer'
		}),
		$close_button = $('<button></button>', {
			'type': 'button',
			'class': 'btn btn-default',
			'data-dismiss': 'modal',
			'html': close_text
		})
		$save_button = $('<button></button>', {
			'type': 'submit',
			'class': 'btn btn-primary',
			'html': save_text
		});

	$modal_footer.append($close_button);
	if ($element.find('.remove-save-button').length == 0) {
		$modal_footer.append($save_button);
	}
	else {
		$element.find('.remove-save-button').remove()
	}
	$modal_footer.append($element.html());
	$element.replaceWith($modal_footer);
};

BASE.addLeadingZeroForElements = function() {
	var $add_leading_zero = $('.add-leading-zero');
	$add_leading_zero.html(BASE.addLeadingZero($add_leading_zero.html()));
};

BASE.prepareLazyLoadImages = function() {
	$('.lazy-load').each(function() {
		var $this = $(this);
		$this.attr('src', $this.data('src'));
	})
};

$(document).ready(function(){
	// Register custom elements
	BASE.registerCustomTag('modal-head', BASE.modalHead);
	BASE.registerCustomTag('modal-body', BASE.modalBody);
	BASE.registerCustomTag('modal-footer', BASE.modalFooter);
	BASE.registerCustomTag('modal-content', BASE.modalContent);
	
	$('#copyright-year').html(new Date().getFullYear());

	// Other base operations
	BASE.removeMe();
	BASE.csrfToken();
	BASE.setTextColor();
	BASE.editableDropdown();
	BASE.setEditableLabels();
	BASE.removeDashedOption();
	BASE.setBackgroundColor();
	BASE.prepareLazyLoadImages();
	BASE.addLeadingZeroForElements();
	BASE.removeLeadingTrailingZeros();
	BASE.checkScrollDependentElements();
	$('.toggle-switch').bootstrapSwitch();
	$('[data-toggle="tooltip"]').tooltip();
	$(window).scroll(BASE.checkScrollDependentElements);
	var clipboard = new Clipboard('.btn-copy');

	$(document)
		.on('submit', 'form.modal-form', function(event) {BASE.submitModalForm(event);})
		.on('keydown', '#editable-field', function(event) {BASE.editableFieldKeyDownCheck(event);})
		.on('click touchstart', '#cancel-button', function() {BASE.returnEditableFieldToPreviousState($(this));})
		.on('click touchstart', '#done-button', function() {BASE.saveNewValueOfEditableField($(this));})
		.on('focus', '.datepicker', function() {$(this).datepicker({ format: 'yyyy-mm-dd' });})
		.on('click touchstart', '.editable-label', BASE.turnLabelIntoField)
		.on('switchChange.bootstrapSwitch', '.save-toggle-switch', function(event, state) {
			BASE.saveNewValueOfToggledSwitch($(this), event, state);})
		.on('click touchstart', '.input-group-addon', function(){$(this).siblings('input').focus();})
		.on('click', '#scroll-to-top', BASE.scrollToTop)
		.on('click', '.language-changer', BASE.changeLanguage)
		.on('click', '.toggle-visibility', BASE.toggleVisibility)
		.on('click', '.btn-copy', BASE.copyText)
		.on('click', '.ajax-button', BASE.ajaxButtonClick)
		.on('click', '#editable-overlay', BASE.editableOverlayClick)
		.on('click', '.demo-alert-close', BASE.closeDemoInfo)
		.on('shown.bs.modal', '.modal', function() {var clipboard = new Clipboard('.btn-copy');});
});
