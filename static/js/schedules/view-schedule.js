var VIEW_SCHEDULE = VIEW_SCHEDULE || {};

VIEW_SCHEDULE.populateDropdownValues = function(e) {
	var $id_year_level = $('#id_year_level');
	if ($id_year_level.val() == null) {
		$id_year_level[0].selectedIndex = 0;
	}

	var $selected_year_level = $id_year_level.find(':selected'),
		$section_dropdown = $('#section-form-group select'),
		$lesson_plan_dropdown = $('#lesson-plan-form-group select'),
		sections = $selected_year_level.data('sections'),
		lesson_plans = $selected_year_level.data('lesson-plans'),
		date_class = $('#same-as-date-class-information').val(),
		year_level = $selected_year_level.data('year-level'),
		is_lesson_plan_existing = false,
		lesson_english = $('#english-lesson').text(),
		hour_english = $('#english-hour').text(),
		same_as_english = $('#english-same-as').text(),
		same_as_japanese = $('#japanese-same-as-outer').text(),
		hour_japanese = $('#japanese-hour-outer').text(),
		$section_select = $('<select></select>', {
			'class':'form-control',
			'name':'section',
			'id': 'id_section'
		}),
		$lesson_plan_select = $('<select></select>', {
			'class':'form-control',
			'name':'lesson_plan',
			'id': 'id_lesson_plan'
		});

	// Last period should show "N/A"
	$('#last-period').html('<i>N/A</i>');
				
	// Populate dropdown for sections
	if (sections.length > 0) {
		for(var item in sections) {
			$section_select.append($('<option></option>', {
				'value':sections[item].id,
				'text':sections[item].section_name
			}));
		}
	}
	else {
		$section_select.append($('<option></option>', {
			'value':'0',
			'text':'There are no sections available for the selected year level.'
		}));
		$section_select.attr('disabled', 'true');
	}

	// Populate dropdown for pre-made lesson plans
	// "Same as" lesson plans
	if (year_level >= 0 && date_class) {
		$('.same-as.year-level-'+year_level+'.'+date_class).each(function() {
			is_lesson_plan_existing = true;
			var $this = $(this),
				id = $this.data('lesson-plan-id'),
				year_level = $this.data('year-level'), 
        		value = '' 
        		lesson_plan_text = $this.find('.lesson-plan-text').text().trim(); 
  			if (year_level == 0) { 
    			year_level = 'SN' 
  			} 
  			value = same_as_english+year_level+', '+lesson_plan_text+same_as_japanese; 
			$lesson_plan_select.append($('<option></option>', {
				'value': id,
				'text': value
			}));
		});
	}

	if (lesson_plans.length > 0) {
		is_lesson_plan_existing = true;
		for(var item in lesson_plans) {
			course_name = '';
			lesson_plan_text = '';

			if (lesson_plans[item].lesson__course__course_name != undefined) {
				course_name = lesson_plans[item].lesson__course__course_name+', ';	
				lesson_plan_text = course_name+lesson_english+lesson_plans[item].lesson__lesson_number+hour_english+lesson_plans[item].hour_number+hour_japanese;
			}
			else {
				lesson_plan_text = lesson_plans[item].topic__name+', Hour '+lesson_plans[item].hour_number;
			}

			$lesson_plan_select.append($('<option></option>', {
				'value':lesson_plans[item].id,
				'text': lesson_plan_text
			}));
		}
	}
	
	// Lesson plan: option none
	var $option_none = $('<option></option>', {
			'value': 0,
			'text': 'None',
			'selected': 'selected',
		});
	BASE.alphabeticallyArrangeOptions($lesson_plan_select.find('option'));
	$option_none.insertBefore($lesson_plan_select.find('option:first-child'));

	if (!is_lesson_plan_existing) {
		$lesson_plan_select.append($('<option></option>', {
			'value':'0',
			'text':'There are no pre-made lesson plans available for the selected year level.'
		}));
		$lesson_plan_select.attr('disabled', 'true');
	}
	
	$section_dropdown.replaceWith($section_select);
	$lesson_plan_dropdown.replaceWith($lesson_plan_select);
};

VIEW_SCHEDULE.clickAddButton = function(e) {
	var $this = $(e.target);
	if ($this.attr('class') == 'glyphicon glyphicon-plus') {
		$this = $this.parent();
	}

	$('#modal-title').html($this.data('title'));
	$('#add-class-school-period-id').val($this.data('school-period-id'));
	$('#add-class-date').val($this.data('date'));

	$('#same-as-date-class-information').val($this.data('date-class'));
	$('#id_year_level')[0].selectedIndex = 0;
	$('#add-edit-class-modal-form').attr('action', '/schedules/add_class');
	VIEW_SCHEDULE.populateDropdownValues();
};

VIEW_SCHEDULE.clickEditButton = function(e) {
	var $this = $(e.target);
	if ($this.attr('class') == 'glyphicon glyphicon-edit') {
		$this = $this.parent();
	}

	var year_level_id = $this.data('school-section-id'),
		section_id = $this.data('section-id'),
		notes = $this.data('notes'), 
		lesson_plan_id = $this.data('lesson-plan-id');

	$('#modal-title').html($this.data('title'));
	$('#add-class-date').val($this.data('date'));
	$('#add-class-section-period-id').val($this.data('section-period-id'));
	$('#add-edit-class-modal-form').attr('action', '/schedules/edit_class');
	$('#same-as-date-class-information').val($this.data('date-class'));
	$('#id_year_level').val(year_level_id);
	$('#id_notes').val(notes); 
	VIEW_SCHEDULE.populateDropdownValues();
	$('#section-form-group select').val(section_id);
	$('#lesson-plan-form-group select').val(lesson_plan_id);
	VIEW_SCHEDULE.showLastPeriod();
};

VIEW_SCHEDULE.showLastPeriod = function() {
	var date = $('#add-class-date').val(),
		section_id = $('#id_section').val(),
		post_url = $('#last-period-url').data('url'),
		month_list = BASE.getLocalizedMonthList(),
		lesson_english = $('#english-lesson').text(),
		hour_english = $('#english-hour').text(),
		on_english = $('#english-on').text(),
		day_japanese = $('#japanese-day-outer').text();

	$.ajax({
		url: post_url,
		method: "POST",
		data: {
			'section_id': section_id,
			'date': date 
		},
		success: function(msg){
			var replace_text = '',
				classes = ''
				return_message = msg.messages,
				$last_period = $('#last-period');

			if (msg.messages.date != null) {
				var last_date = new Date(return_message.date),
					year = last_date.getFullYear(),
					month_name = month_list[last_date.getMonth()],
					date_text = month_name+' '+last_date.getDate()+day_japanese+year;

				replace_text = lesson_english+return_message.lesson+hour_english+return_message.hour+on_english+date_text;
				classes = 'last-class-present';
			}
			else {
				replace_text = 'No classes have been held yet for the specified section.';
				classes = 'last-class-absent';
			}

			$last_period.attr('class', classes);
			$last_period.html(replace_text);
		},
		error: function(msg){
			console.log('AJAX modal form validation failure. The URL used was: '+ post_url);
		}
	});
};

$(document).ready(function(){
	$(document)
		.on('change', '#id_year_level', VIEW_SCHEDULE.populateDropdownValues)
		.on('change', '#id_section', VIEW_SCHEDULE.showLastPeriod)
		.on('change', '#id_year_level', VIEW_SCHEDULE.showLastPeriod)
		.on('mousedown', '.add-class-button', VIEW_SCHEDULE.clickAddButton)
		.on('mousedown', '.edit-class-button', VIEW_SCHEDULE.clickEditButton);
});