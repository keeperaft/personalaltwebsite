var CALENDAR_EDIT = CALENDAR_EDIT || {},
    undoable_actions = [],
    undoable_action_id = 0,
    undoable_action_color = "",
    is_saving = false,
    is_unsaved = false,
    is_shift_pressed = false,
    is_ctrl_pressed = false,
    is_z_pressed = false,
    is_s_pressed = false,
    is_mouse_down = false,
    calendar_shift_source = null;

var KEY_SHIFT = 16,
    KEY_CTRL = 17,
    KEY_Z = 90,
    KEY_S = 83;

CALENDAR_EDIT.activeDropdownChanged = function(e) {
    var $selected_element = $(e.target).find(':selected'),
        $edit_school_color = $('#edit-school-color');
    $edit_school_color.css('background-color', $selected_element.data('color'));
    $edit_school_color.data('selected-value', $selected_element.val());
};
CALENDAR_EDIT.loadInstructionImages = function(e) {
    var $this = $(e.target),
        $element = $($this.data('target')),
        image_src_base = $this.data('image-url');

    // We only need to load the images once.
    if($this.data('has-been-clicked') === false) {
        $this.data('has-been-clicked', true);
        var $row = null,
            $instructions = $('<div></div>', {
                'class': 'toggle-visibility-target',
                'id': 'instructions'
            });
        $element.children('ul').children('li').each(function(index, value) {
            if (index % 2 === 0) {
                $row = $('<div></div>', {
                    'class': 'row',
                });
            }
            var $instruction_div = $('<div></div>', {
                    'class': 'instruction-image',
                    'html': $('<img>', {
                        'src': image_src_base+parseInt(index+1)+'.gif',
                        'alt': 'Loading...'
                    })
                }),
                $instruction_text = $('<div></div>', {
                    'class': 'instruction-text',
                    'text': $(value).html()
                }),
                $main_half_div = $('<div></div>', {
                    'class': 'col-sm-6'
                });
            $main_half_div.append($instruction_div);
            $main_half_div.append($instruction_text);
            $row.append($main_half_div);
            if (index % 2 == 1) {
                $instructions.append($row);
            }
        });
        $element.replaceWith($instructions);
    }    
};
CALENDAR_EDIT.saveToDatabase = function() {
    if (is_saving === false) {
        is_saving = true;
        var $calendar_data = $('#calendar-data'),
            $calendar_overlay = $('.calendar-overlay'),
            $fixed_saving = $('.fixed-saving'),
            post_url = $calendar_data.data('url'),
            value = $calendar_data.data('calendar-data'),
            school_year_id = $calendar_data.data('school-year-id'),
            scroll_pixels_from_top = $(window).scrollTop();
        
        // Disable the calendar and show the "Saving..."
        $calendar_overlay.css('display', 'block');
        
        // Prepare the URL and values to be passed
        var scroll_to_top_save_pixels = 325;
        if (scroll_pixels_from_top >= scroll_to_top_save_pixels) {
            $fixed_saving.css('display', 'block');
        }

        $.ajax({
            url: post_url,
            method: "POST",
            data: {
                'value': value,
                'school_year_id': school_year_id
            },
            success: function(msg){
                // If saving is successful: 
                // 1. Re-enable the calendar
                // 2. Remove the "saving..."
                // 3. Display the success message.
                is_saving = false;
                if (msg.is_success === true) {
                    $calendar_overlay.css('display', 'none');
                    $fixed_saving.css('display', 'none');
                    is_unsaved = false;
                    
                    BASE.showNotification(NOTIFICATION_SUCCESS, msg.messages);
                }
                // Else, display whatever errors there are within the modal
                else {
                    console.log("Saving unsuccessful.");
                }
                
            },
            error: function(msg){
                is_saving = false;
                console.log('AJAX modal form validation failure. The URL used was: '+ post_url);
            }
        }); 
    }
};
CALENDAR_EDIT.undoLastAction = function() {
    if (is_saving === false && undoable_actions.length > 0) {
        var $edit_school_color = $('#edit-school-color'),
            current_color = $edit_school_color.css('background-color\n'),
            current_id = $edit_school_color.data('selected-value\n');

        $edit_school_color.css('background-color', undoable_action_color);
        $edit_school_color.data('selected-value', undoable_action_id);

        for (var index in undoable_actions) {
            calendar_shift_source = null;
            CALENDAR_EDIT.toggleCalendarDay(undoable_actions[index], false, null);
        }

        undoable_actions = [];
        undoable_action_id = 0;
        undoable_action_color = "";

        $edit_school_color.css('background-color', current_color);
        $edit_school_color.data('selected-value', current_id);
    }
};
CALENDAR_EDIT.toggleCalendarDay = function(e, local_is_shift_pressed, local_calendar_shift_source) {
    is_unsaved = true;
    var $element = $(e);

    // Shift + Click
    if (local_is_shift_pressed && local_calendar_shift_source !== null) {
        var date_source = new Date(local_calendar_shift_source),
            date_destination = new Date($element.attr('id'));
        
        date_source.setHours(0);
        date_destination.setHours(0);

        var current_date = date_source,
            date_increment = 1;
        
        if (current_date > date_destination) {
            date_increment = -1;
        }

        // CTRL+Z
        undoable_actions.push($('#'+local_calendar_shift_source));

        while(current_date.valueOf() != date_destination.valueOf()) {
            current_date = new Date(current_date);
            current_date.setDate(current_date.getDate() + date_increment);

            var current_month = current_date.getMonth() + 1,
                month_leading_zero = BASE.addLeadingZero(current_month),
                day_leading_zero = BASE.addLeadingZero(current_date.getDate());

            var selector_id = [];
            selector_id.push('#');
            selector_id.push(current_date.getFullYear());
            selector_id.push('-');
            selector_id.push(month_leading_zero);
            selector_id.push('-');
            selector_id.push(day_leading_zero);
            CALENDAR_EDIT.toggleCalendarDay($(selector_id.join('')), false, null);
        }
    }
    else {
        var $edit_school_color = $('#edit-school-color'),
            $calendar_data = $('#calendar-data'),
            color_array = $element.data('color-array'),
            new_color = BASE.rgbTohex($edit_school_color.css('background-color')),
            current_id = $edit_school_color.data('selected-value'),
            new_date = $element.attr('id');

        color_array = color_array === null ? '[]' : color_array;

        // For CTRL + Z
        undoable_action_color = new_color;
        undoable_action_id = current_id;
        undoable_actions.push(e);

        // Add the current date in the json list
        if (date_json[current_id] == null) {
            date_json[current_id] = [];
        }

        // If the new color exists within the array, remove it. If not, insert it.
        var color_index = color_array.indexOf(new_color),
            date_index = date_json[current_id].indexOf(new_date),
            is_exists_color = color_index > -1,
            is_exists_date = date_index > -1;

        if (is_exists_color) {
            color_array.splice(color_index, 1);
        }
        else {
            color_array.push(new_color);
        }
        if (is_exists_date) {
            date_json[current_id].splice(date_index, 1);
        }
        else {
            date_json[current_id].push(new_date);
        }

        // Set JSON date to calendar data element
        $calendar_data.data('calendar-data', JSON.stringify(date_json));

        // Set the color array
        $element.attr('data-color-array', JSON.stringify(color_array)); 

        // Go through the array and recolor 
        var background_string = [],
            color_count = color_array.length,
            percentage_current = 0,
            percentage_increment = 100/color_count;

        if (color_count > 0) {
            background_string.push("linear-gradient(to bottom, ");
        }
        else {
            $element.attr('style', '');
        }

        for (var index in color_array) {
            var current_color = color_array[index];
            background_string.push(current_color);
            background_string.push(" ");
            background_string.push(percentage_current);
            background_string.push("%, ");

            percentage_current += percentage_increment;
            background_string.push(current_color);
            background_string.push(" ");
            background_string.push(percentage_current);
            background_string.push("%");

            if (index != color_count - 1) {
                background_string.push(", ");
            }
        }

        if (color_count > 0) {
            background_string.push(")");
            $element.css('background', background_string.join(''));           
        } 
    }
};
CALENDAR_EDIT.windowScroll = function() {
    // Get current scroll position
    var scroll_pixels_from_top = $(window).scrollTop(),
        $edit_schedule_container = $('.edit-schedule-container'),
        $edit_schedule_row = $('.edit-schedule-row'),
        $fixed_saving = $('.fixed-saving'),
        scroll_to_top_pixels = 200,
        scroll_to_top_save_pixels = 350;

    if (scroll_pixels_from_top >= scroll_to_top_save_pixels && is_saving === true) {
        $fixed_saving.css('display', 'block');
    }
    else {
        $fixed_saving.css('display', 'none');
    }

    if (scroll_pixels_from_top >= scroll_to_top_pixels) {
        if($edit_schedule_container.length === 0) {
            $edit_schedule_row.css('position', 'fixed');
            $edit_schedule_row.css('top', '0px');
            $edit_schedule_row.css('background-color', '#FFF');
            $edit_schedule_row.css('border-radius', '0 0 5px 5px');
            $edit_schedule_row.css('z-index', '2');
            $edit_schedule_row.css('box-shadow', '-2px 4px 5px #AAA');
            $edit_schedule_row.addClass('container');
         }
    }
    else {
        $edit_schedule_row.removeClass('container');
        $edit_schedule_row.css('position', 'relative');
        $edit_schedule_row.css('top', 'auto');
        $edit_schedule_row.css('background-color', 'auto');
        $edit_schedule_row.css('border-radius', '0px');
        $edit_schedule_row.css('z-index', '0');
        $edit_schedule_row.css('box-shadow', 'none');
     }
};
CALENDAR_EDIT.keyDown = function(event) {
    var code = event.keyCode || event.which;
    is_shift_pressed = code == KEY_SHIFT ? true : is_shift_pressed;
    is_ctrl_pressed = code == KEY_CTRL ? true : is_ctrl_pressed;
    is_z_pressed = code == KEY_Z ? true : is_z_pressed;
    is_s_pressed = code == KEY_S ? true : is_s_pressed;

    if (is_ctrl_pressed && is_z_pressed) {
        CALENDAR_EDIT.undoLastAction();
    }

    if (is_ctrl_pressed && is_s_pressed) {
        event.preventDefault();
        CALENDAR_EDIT.saveToDatabase();
    }
};
CALENDAR_EDIT.keyUp = function(event) {
    var code = event.keyCode || event.which;
    is_shift_pressed = code == KEY_SHIFT ? false : is_shift_pressed;
    is_ctrl_pressed = code == KEY_CTRL ? false : is_ctrl_pressed;
    is_z_pressed = code == KEY_Z ? false : is_z_pressed;
    is_s_pressed = code == KEY_S ? false : is_s_pressed;
};
CALENDAR_EDIT.clickDay = function(e) {
    var $this = $(e.target);
    if ($this.data('is-editing') === true && $this.data('is-entered') === false) {
        CALENDAR_EDIT.toggleCalendarDay($this, is_shift_pressed, calendar_shift_source);       
        calendar_shift_source = $this.attr('id');
    } 
};
CALENDAR_EDIT.mouseMoveDay = function(e) {
    var $this = $(e.target);
    if ($this.data('is-editing') === true && is_mouse_down && $this.data('is-entered') === false) {
        $this.data('is-entered', true);
        CALENDAR_EDIT.toggleCalendarDay($this, is_shift_pressed, calendar_shift_source);       
        calendar_shift_source = $this.attr('id');
    }
};
CALENDAR_EDIT.mouseDownDay = function() {
    undoable_actions = [];
};
CALENDAR_EDIT.mouseLeaveDay = function(e) {
    $(e.target).data('is-entered', false);
};
CALENDAR_EDIT.showLeaveConfirmationMessage = function() {
    if(is_unsaved){
        return "You have unsaved changes on this page. Do you want to leave this page and discard your changes or stay on this page?";
    }
};

$(document).ready(function() {
    $('#edit-school-color').css('background-color', $('#edit-school-color').data('default-color'));

    $(window)
        .scroll(CALENDAR_EDIT.windowScroll)
        .bind('beforeunload', CALENDAR_EDIT.showLeaveConfirmationMessage);

    $(document)
        .on('click', '#toggle-instructions', CALENDAR_EDIT.loadInstructionImages)
        .on('click', '#btn-undo', CALENDAR_EDIT.undoLastAction)
        .on('click', '#btn-save', CALENDAR_EDIT.saveToDatabase)
        .on('click', '.days li', CALENDAR_EDIT.clickDay)
        .on('mousemove', '.days li', CALENDAR_EDIT.mouseMoveDay)
        .on('mousedown', '.days li', CALENDAR_EDIT.mouseDownDay)
        .on('mouseleave', '.days li', CALENDAR_EDIT.mouseLeaveDay)
        .on('change', '.active-school-dropdown select', CALENDAR_EDIT.activeDropdownChanged)
        .on('keydown', function(event){CALENDAR_EDIT.keyDown(event);})
        .on('keyup', function(event){CALENDAR_EDIT.keyUp(event);})
        .on('mousedown', function() { is_mouse_down = true; })
        .on('mouseup', function() { is_mouse_down = false; });
});