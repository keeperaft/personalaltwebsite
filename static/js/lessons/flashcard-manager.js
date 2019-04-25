var FLASHCARDS = FLASHCARDS || {};

FLASHCARDS.search = function() {
	var href = '/lessons/search_flashcard/'+encodeURI($('#search-term').val());
	$('#a-search-flashcard').attr('href', href)
};

FLASHCARDS.checkKey = function(){
	$('#search-term').keyup(function(e){
	    if(e.keyCode == 13) {
	        $('#btn-search-flashcard').click();
	    }
	});
};

$(document).ready(function() {
	$(document)
		.on('change', '#search-term', FLASHCARDS.search)
		.on('keyup', '#search-term', FLASHCARDS.checkKey);
});