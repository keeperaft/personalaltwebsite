var VIEW_SECTION_PERIOD = VIEW_SECTION_PERIOD || {};

VIEW_SECTION_PERIOD.prepareModalDropdowns = function() {
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

VIEW_SECTION_PERIOD.prepareLessonPlanInformationPage = function() {
	$('.btn-primary-view-section-period').each(function() {
		$(this).attr('class', 'btn btn-primary');
	});
};

$(document).ready(function(){
	VIEW_SECTION_PERIOD.prepareModalDropdowns();
	VIEW_SECTION_PERIOD.prepareLessonPlanInformationPage();
	
});