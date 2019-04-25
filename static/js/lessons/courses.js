var COURSES = COURSES || {};

COURSES.prepareLastLessonNumber = function() {
	var $span_last_lesson_number = $('.lesson-number').last(),
		last_lesson_number = parseInt($span_last_lesson_number.html());

	if(isNaN(last_lesson_number)) {
		last_lesson_number = 1;
	}
	else {
		last_lesson_number += 1;
	}
	$('#new-lesson-number').html(last_lesson_number);
	$('#new-lesson-number-input').val(last_lesson_number);
};

COURSES.displayPicture = function(event) {
	var file = event.target.files[0],
		$preview_image = $('.modal.fade.in .add-flashcard-preview-image');

	if (file.type.match('image.*')) {
		var reader = new FileReader();
		reader.onload = (function(file_information) {
			return function(e) {
				$preview_image.attr('src', e.target.result);
			};
		})(file);
		reader.readAsDataURL(file);
	}
	else {
		// Display an error and remove the file
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

		$unordered_list.append($('<li></li>', {
			'text': 'Error: The uploaded file is not an image. Please upload an image file.'
		}));

		$error_message.append($close_button);
		$error_message.append($unordered_list);
		$('.modal.fade.in .modal-messages').append($error_message);
		$preview_image.attr('src', $preview_image.data('original-src'));
		$(event.target).val('');
	}
}

$(document).ready(function() {
	COURSES.prepareLastLessonNumber();

	$(document).on('change', '#id_picture', COURSES.displayPicture);
});