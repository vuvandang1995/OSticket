$(function() {
    "use strict";
    $('.year-calendar').pignoseCalendar({
        theme: 'blue', // light, dark, blue
        select: function(date, context) {
            group_agent_Socket.send(JSON.stringify({
                'message' : JSON.stringify(date[0]).split('T')[0].substring(1),
                'time' : 'date',
            }));
        }
    });

    $('input.calendar').pignoseCalendar({
        format: 'YYYY-MM-DD' // date format string. (2017-02-02)
    });

    //alert(('body .year-calendar .pignose-calendar-body .pignose-calendar-row .pignose-calendar-unit-date').children('a').html());
});

