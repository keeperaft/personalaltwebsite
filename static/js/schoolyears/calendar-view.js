var CALENDAR_VIEW = CALENDAR_VIEW || {},
    date_json = null,
    info_json = null;

CALENDAR_VIEW.downloadIcsFile = function() {
    var ics_content = [],
        school_year_name = $('#school-year-name').html().trim(),
        today = new Date(),
        current_year = today.getFullYear(),
        current_month = BASE.addLeadingZero(today.getMonth()+1),
        current_day = BASE.addLeadingZero(today.getDay()),
        current_hour = BASE.addLeadingZero(today.getHours()),
        current_minute = BASE.addLeadingZero(today.getMinutes()),
        current_seconds = BASE.addLeadingZero(today.getSeconds()),
        current_date = [],
        current_date_string = current_date.join(''),
        filename_array = [];

    // ICS Header
    ics_content.push('BEGIN:VCALENDAR\n');
    ics_content.push('PRODID://PAW//PersonalALTWebsite//EN\n');
    ics_content.push('VERSION:2.0\n');
    ics_content.push('CALSCALE:GREGORIAN\n');
    ics_content.push('METHOD:PUBLISH\n');

    ics_content.push('X-WR-CALNAME:Work Schedule ');
    ics_content.push(school_year_name);
    ics_content.push('\n');
    ics_content.push('X-WR-TIMEZONE:Asia/Tokyo\n');
    ics_content.push('X-WR-CALDESC:Work Schedule for ');
    ics_content.push(school_year_name);
    ics_content.push('\n');

    ics_content.push('BEGIN:VTIMEZONE\n');
    ics_content.push('TZID:Asia/Tokyo\n');
    ics_content.push('X-LIC-LOCATION:Asia/Tokyo\n');
    ics_content.push('BEGIN:STANDARD\n');
    ics_content.push('TZOFFSETFROM:+0900\n');
    ics_content.push('TZOFFSETTO:+0900\n');
    ics_content.push('TZNAME:JST\n');
    ics_content.push('DTSTART:19700101T000000\n');
    ics_content.push('END:STANDARD\n');
    ics_content.push('END:VTIMEZONE\n\n');

    current_date.push(current_year);
    current_date.push(current_month);
    current_date.push(current_day);
    current_date.push('T');
    current_date.push(current_hour);
    current_date.push(current_minute);
    current_date.push(current_seconds);
    current_date.push('Z');
    current_date_string = current_date.join('')
    
    filename_array.push(current_year);
    filename_array.push(current_month);
    filename_array.push(current_day);
    filename_array.push('-');
    filename_array.push(current_hour);
    filename_array.push(current_minute);
    filename_array.push(current_seconds);
    filename_array.push('.ics');

    for (var school_id in date_json) {
        for (var date_index in date_json[school_id]) {
            var address = info_json[school_id].address, 
                date = date_json[school_id][date_index],
                next_day = new Date(date),
                date_array = date.split('-'),
                ics_array_date_start = [],
                ics_array_date_end = [];

            if (address === '') {
                address = 'N/A';
            }

            next_day.setDate(next_day.getDate()+1);
            ics_array_date_start.push(date_array[0]); //year
            ics_array_date_start.push(BASE.addLeadingZero(date_array[1])); //month
            ics_array_date_start.push(BASE.addLeadingZero(date_array[2])); //day

            ics_array_date_end.push(next_day.getFullYear()); //year
            ics_array_date_end.push(BASE.addLeadingZero(next_day.getMonth()+1)); //month
            ics_array_date_end.push(BASE.addLeadingZero(next_day.getDate())); //day

            var ics_string_date_start = ics_array_date_start.join(''); // Used multiple times

            ics_content.push('BEGIN:VEVENT\n');
            ics_content.push('DTSTART;VALUE=DATE:');
            ics_content.push(ics_string_date_start);
            ics_content.push('\n');
            ics_content.push('DTEND;VALUE=DATE:');
            ics_content.push(ics_array_date_end.join(''));
            ics_content.push('\n');
            ics_content.push('DTSTAMP:');
            ics_content.push(current_date_string);
            ics_content.push('\n');

            ics_content.push('ORGANIZER:PersonalALTWebsite\n');
            ics_content.push('UID:');
            ics_content.push(school_id);
            ics_content.push(ics_string_date_start);
            ics_content.push('\n');
            ics_content.push('LOCATION:');
            ics_content.push(address);
            ics_content.push('\n');
            ics_content.push('SUMMARY:');
            ics_content.push(info_json[school_id].name);
            ics_content.push('\n');
            ics_content.push('END:VEVENT\n\n');
        }
    }

    ics_content.push('END:VCALENDAR\n');
    var text = ics_content.join(''),
        filename = filename_array.join(''),
        blob = new Blob([text], {type: "text/plain;charset=utf-8"});
    saveAs(blob, filename);
};

CALENDAR_VIEW.calendarDisplay = function(e) {
    var $element = $(e),
        $calendar_days = $('<div></div>'),
        $legends_content = $('<div></div>'),    // TO-DO: Make it so that all the legends are available from the very beginning
        $main_calendar_content = $('<div></div>'),
        $month_days = null,
        $row = null,
        $main_half_div = null,
        $temporary_calendar = $('.multi-select-calendar'),
        $calendar_month_element = $temporary_calendar.find('.schoolyear-month'),
        start_year = $element.data('start-year'),
        start_month = $element.data('start-month'),
        end_year = $element.data('end-year'),
        end_month = $element.data('end-month'),
        is_editing = $element.data('is-editing'),
        month_count = BASE.getMonthCount(start_year, end_year, start_month, end_month);                        


    // To-do: Investigate django-JS Localization
    // https://docs.djangoproject.com/en/1.11/topics/i18n/translation/#internationalization-in-javascript-code
    var month_list = BASE.getLocalizedMonthList();

    // Build the inner divs
    info_json = $element.data('id-info-map');
    date_json = $element.data('calendar-data');

    for(var school_id in date_json) {
        for(var inner_key in date_json[school_id]) {
            $calendar_days.append($('<div></div>', {
                'class': date_json[school_id][inner_key],
                'data-color': info_json[school_id].color
            }));
        }
        $legends_content.append($('<div></div>', {
            'class': 'legends-school-color',
            'style': 'background-color:#'+info_json[school_id].color,
            'text': info_json[school_id].name
        }));
    }

    $main_calendar_content.append($legends_content);

    for(var i=0; i<month_count; i++) {
        var month_index = start_month + i - 1,
            month_ordinal_raw = (start_month + i)%12,
            month_ordinal = month_ordinal_raw === 0 ? 12 : month_ordinal_raw,
            name_year = start_year + Math.floor(month_index/12),
            name_month = month_list[month_index%12],
            count_days = BASE.dayCount(month_ordinal, name_year),
            month_leading_zero = BASE.addLeadingZero(month_ordinal),
            weekday_of_first_day = new Date(name_year+"-"+month_leading_zero+"-01").getDay();

        if (i % 2 === 0) {
            $row = $('<div></div>', {'class': 'row'});
        }

        $calendar_month_element.html(name_month+" "+name_year);
        $main_half_div = $('<div></div>', {'class': 'col-sm-6'});
        $main_half_div.append($temporary_calendar.html());
        $month_days = $('<ul></ul>', {'class': 'days'});

        for(var j=0; j<weekday_of_first_day; j++) {
            $month_days.append($('<li></li>', {'class': 'no-day'}));
        }
        
        for(var current_day=1; current_day<=count_days; current_day++) {
            var $li_element = $('<li></li>', {}),
                day_leading_zero = BASE.addLeadingZero(current_day),
                selector = "."+name_year+"-"+month_leading_zero+"-"+day_leading_zero,
                color_array = [], 
                $selected_classes = $calendar_days.find(selector),  
                selector_count = $selected_classes.length,
                background_string = [],
                percentage_current = 0,
                percentage_increment = 100/selector_count;
            
            $li_element.html(current_day);
            if (selector_count > 0) {
                background_string.push("linear-gradient(to bottom, ");
            }

            $selected_classes.each(function(index) {
                var current_color = '#'+$(this).data('color');
                color_array.push(current_color);
                background_string.push(current_color);
                background_string.push(" ");
                background_string.push(percentage_current);
                background_string.push("%, ");

                percentage_current += percentage_increment;
                background_string.push(current_color);
                background_string.push(" ");
                background_string.push(percentage_current);
                background_string.push("%");

                if (index != selector_count - 1) {
                    background_string.push(", ");
                }
            });

            if (is_editing === true) {
                $li_element.addClass('cursor-pointer');
                $li_element.attr('id', name_year+"-"+month_leading_zero+"-"+day_leading_zero);
                $li_element.attr('data-is-editing', 'true');
                $li_element.attr('data-is-entered', 'false');
                $li_element.attr('data-color-array', JSON.stringify(color_array));
            } 

            if (selector_count > 0) {
                background_string.push(")");
                $li_element.attr('style', 'background:'+background_string.join(''));           
            }

            $month_days.append($li_element);
        }

        $main_half_div.append($month_days);
        $row.append($main_half_div);

        if (i % 2 == 1 || i == month_count - 1) {
            $main_calendar_content.append($row);
            $main_calendar_content.append($('<br/>', {}));
        }
    }
    
    $element.replaceWith($main_calendar_content);
};

$(document).ready(function() {
    BASE.registerCustomTag('calendar-display', CALENDAR_VIEW.calendarDisplay);
    $(document).on('click', '#btn-download-ics', CALENDAR_VIEW.downloadIcsFile);
});