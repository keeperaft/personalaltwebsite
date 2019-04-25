var SCHOOL_YEAR = SCHOOL_YEAR || {};

SCHOOL_YEAR.prepareSchoolColor = function($element) {
    var color_content = [];
    color_content.push('#');
    color_content.push($element.data('color'));
    $element.css('background-color', color_content.join(''));
};
SCHOOL_YEAR.prepareSchoolColorModal = function(e) {
    // Uncheck all colors
    var $this = $(e.target),
        $school_color_selected = $('.school-color-selected'),
        $color_checkmark = $('.color-checkmark'),
        $modal_school_color = $('.modal-school-color'),
        $color_value = $('#color-value'),
        $color_id = $('#color-id'),
        current_color = $this.data('color'),
        current_id = $this.data('id');

    $school_color_selected.each(function() {
        $(this).attr('class', 'btn modal-school-color school-color color-form');
    });
    $color_checkmark.each(function() {
        $(this).css('display', 'none');
    })

    // Set the appropriate classes as checked, based on data-color
    $modal_school_color.each(function() {
        var $modal_school_color_element = $(this);
        var selectable_color = $modal_school_color_element.data('color');
        $modal_school_color_element.data('id', current_id);
        if (current_color == selectable_color) {
            $modal_school_color_element.attr('class', 'btn modal-school-color school-color school-color-selected color-form');
            $modal_school_color_element.find('.color-checkmark').css('display', 'block');

            // Pre-fill the text field with the appropriate color
            $color_value.val($modal_school_color_element.data('key'));
            $color_id.val(current_id)
        }
    });
};
SCHOOL_YEAR.colorFormClick = function(e) {
    $('#color-value').val($(this).data('key'));
}
SCHOOL_YEAR.calculateTotalCostOnChangeCheckbox = function($this) {
    var id = $this.data('id'),
        initial_cost = parseInt($('#initial-total-cost-'+id).html());
    SCHOOL_YEAR.calculateTotalCostOnChange(id, initial_cost);
};
SCHOOL_YEAR.calculateTotalCostOnChange = function(id, initial_cost){
    var is_round_trip = $('#is-round-trip-'+id).bootstrapSwitch('state'),
        post_url = '/schoolyears/update_route/calculated_total_cost/',
        calculated_cost = initial_cost;

    if (is_round_trip) {
        calculated_cost = initial_cost*2;
    }
    $('#calculated-total-cost-'+id).html(calculated_cost);

    $.ajax({
        url: post_url,
        method: "POST",
        data: {
            'id': id,
            'value': calculated_cost 
        },
        success: function(msg){
            // Show success notification
            // showNotification(NOTIFICATION_SUCCESS, msg.messages)
        },
        error: function(msg){
            // Show error notification
            BASE.showNotification(NOTIFICATION_FAILURE, msg.messages);
        }
    });
};
SCHOOL_YEAR.calculateTotalCostOnChangeInput = function($this) {
    var id = $this.find('span:first').data('id'),
        initial_cost = $('#initial-total-cost-'+id+' input').val();
    SCHOOL_YEAR.calculateTotalCostOnChange(id, initial_cost);
};

$(document).ready(function(){
    $('.school-color').each(function() { SCHOOL_YEAR.prepareSchoolColor($(this)); });
    $(document)
        .on('click', '.school-color', SCHOOL_YEAR.prepareSchoolColorModal)
        .on('click', '.color-form', SCHOOL_YEAR.colorFormClick)
        .on('switchChange.bootstrapSwitch', '.cost-toggle-switch', function() {SCHOOL_YEAR.calculateTotalCostOnChangeCheckbox($(this));})
        .on('change', '.route-cost', function() {SCHOOL_YEAR.calculateTotalCostOnChangeInput($(this));})
        
});
