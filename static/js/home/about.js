var ABOUT = ABOUT || {};

ABOUT.loadAboutImages = function() {
	// Calculate the options for month from the given start and end months and years
	var is_english = $('#active-language').text() == 'en';
	$('.about-image-container').each(function(){
		var $this = $(this),
			image_src = $this.data('en');
		if (!is_english) {
			image_src = $this.data('ja');
		}
		var image = $('<img></img>', {
				'src':image_src,
				'class':'about-image',
				'alt':'Loading...'
			});
		$this.replaceWith(image);
	})

};

$(document).ready(function(){
	ABOUT.loadAboutImages();
});