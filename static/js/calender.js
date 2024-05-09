// calendar.js

document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        selectable: true, // allow selecting dates
        select: function(info) {
            var title = prompt('Enter event title:');
            if (title) {
                calendar.addEvent({
                    title: title,
                    start: info.startStr,
                    end: info.endStr,
                    allDay: info.allDay
                });
            }
        }
    });
    calendar.render();

    // Add event button functionality
    document.getElementById('addEventBtn').addEventListener('click', function() {
        var title = prompt('Enter event title:');
        if (title) {
            calendar.addEvent({
                title: title,
                start: new Date(),
                allDay: true
            });
        }
    });
});
