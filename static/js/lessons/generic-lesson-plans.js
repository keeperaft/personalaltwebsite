var GENERIC_LESSON_PLANS = GENERIC_LESSON_PLANS || {};

GENERIC_LESSON_PLANS.changeButtonHref = function(e) {
	var topic_id = $('#topic-selection').find(':selected').val(),
		href = '/lessons/generic_lesson_plans/'+topic_id,
		$link = $('#check-lesson-plan-link'),
		$button = $('#check-lesson-plan-button');

	if (topic_id == 0) {
		$button.attr('disabled', 'disabled');
	}
	else {
		$button.removeAttr('disabled');
	}
	$link.attr('href', href);
}

GENERIC_LESSON_PLANS.prepareLastHourNumber = function() {
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

GENERIC_LESSON_PLANS.prepareModalDropdowns = function() {
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

$(document).ready(function(){
	GENERIC_LESSON_PLANS.prepareLastHourNumber();
	GENERIC_LESSON_PLANS.changeButtonHref();
	GENERIC_LESSON_PLANS.prepareModalDropdowns();

	$(document).on('change', '#topic-selection', GENERIC_LESSON_PLANS.changeButtonHref);
});