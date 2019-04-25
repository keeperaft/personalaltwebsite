var LESSON_PLANS = LESSON_PLANS || {};

LESSON_PLANS.populateDropdownValues = function() {
	var $selected_course = $('#lesson-plan-course').find(':selected'),
		$lesson_dropdown_cell = $('#lesson-plan-lesson-dropdown-cell'),
		selected_lesson_id = $lesson_dropdown_cell.data('selected-id'),
		lessons = $selected_course.data('lessons'),
		$select = $('<select></select>', {
			'class':'form-control',
			'name':'lesson_id'
		});

	if (lessons.length > 0) {
		// Populate dropdown for lessons
		for(var item in lessons) {
			var lesson = lessons[item],
				lesson_id = lesson['id'],
				$option = $('<option></option>', {
					'value':lesson['id'],
					'text': 'Lesson '+lesson['lesson_number']+': '+lesson['title']
				});
			if (selected_lesson_id == lesson_id) {
				$option.attr('selected', 'selected')
			}
			$select.append($option);
		}
	}
	else {
		$select.append($('<option></option>', {
			'value':'0',
			'text':'No lessons available for this book. Please add a lesson.'
		}));
		$select.attr('disabled', 'true');
	}

	$lesson_dropdown_cell.html($select);
};

LESSON_PLANS.prepareModalDropdowns = function() {
	$('.lesson-plan-form .form-group select').each(function() {
		var $this = $(this),
			$options = $this.find('option:gt(0)'),
			$all_options = $this.find('option');

		if ($options.length == 0) {
			$this.replaceWith($('<select></select>', {
				'class':'form-control',
				'name': 'none',
				'html': $('<option></option>', {
					'html': 'There are no activities available for this portion.'
				}),
				'disabled': 'disabled',
			}));
		}
		else {
			// Remove the dash select if it exists.
			$all_options.each(function() {
				var $option = $(this);
				if ($option.html() == '---------') {
					$option.remove();
				}
			});
			var $option_none = $('<option></option>', {
				'value': 0,
				'text': 'None'
			});
			BASE.alphabeticallyArrangeOptions($this.find('option'));
			$option_none.insertBefore($this.find('option:first-child'));
		}
	});
};

LESSON_PLANS.changeLessonPlanButtonHref = function(e) {
	var lesson_id = $('#lesson-plan-lesson-dropdown-cell select').find(':selected').val(),
		href = '/lessons/lesson_plans/'+lesson_id,
		$link = $('#check-lesson-plan-button'),
		$link_button = $link.find('.btn-primary');

	if (lesson_id == 0) {
		$link_button.attr('disabled', 'disabled');
	}
	else {
		$link_button.removeAttr('disabled');
	}

	$link.attr('href', href);
}

LESSON_PLANS.prepareLastHourNumber = function() {
	var $span_hour_lesson_number = $('.hour-number').last(),
		last_hour_number = parseInt($span_hour_lesson_number.html());

	if(isNaN(last_hour_number)) {
		last_hour_number = 1;
	}
	else {
		last_hour_number += 1;
	}
	$('#new-hour-number').html(last_hour_number);
	$('#new-hour-number-input').val(last_hour_number);
};

$(document).ready(function(){
	LESSON_PLANS.populateDropdownValues();
	LESSON_PLANS.prepareModalDropdowns();
	LESSON_PLANS.prepareLastHourNumber();
	LESSON_PLANS.changeLessonPlanButtonHref();
	BASE.alphabeticallyArrangeOptions($('#lesson-plan-course').find('option'));

	$(document)
		.on('change', '#lesson-plan-course', LESSON_PLANS.populateDropdownValues)
		.on('change', '#lesson-plan-lesson-dropdown-cell > select', LESSON_PLANS.changeLessonPlanButtonHref)
		.on('change', '#lesson-plan-course', LESSON_PLANS.changeLessonPlanButtonHref);
});