var FLASHCARDS = FLASHCARDS || {};

FLASHCARDS.prepareFlashcardImage = function($element) {
	var flashcard_id = $element.data('flashcard-id'),
		$image_wrapper = $('#edit-flashcard-'+flashcard_id+' .flashcard-image-wrapper'),
		$image = $('<img/>', {
			'class':'flashcard-preview-image',
			'src':$image_wrapper.data('image'),
			'alt':'No preview image',
		}),
		$loading_text = $('#loading-text');
	$image_wrapper.html($image);

	$loading_text.show();
	$image.on('load', function(){
		$loading_text.hide();
	})
};

$(document).ready(function() {
	$('#loading-text').hide();
	$(document).on('click', '.edit-flashcard-button', function() {FLASHCARDS.prepareFlashcardImage($(this));})
});