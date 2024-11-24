var calendarEl = document.getElementById('calendar');
var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',  // Vista inicial del calendario (mes)
    locale: 'es',  // Configurar el idioma en español
    events: function(fetchInfo, successCallback, failureCallback) {
        $.ajax({
            url: '/api/eventos-y-feriados/',  // URL de la API para obtener los eventos
            method: 'GET',
            success: function(data) {
                // Filtrar los eventos por el tipo seleccionado
                var selectedType = $('#event-type-filter').val();
                var events = data.filter(function(event) {
                    return selectedType === "" || event.tipo === selectedType;
                }).map(function(event) {
                    return {
                        id: event.id,
                        title: event.titulo,
                        start: event.fecha_inicio,
                        end: event.fecha_finalizacion,
                        description: event.descripcion,
                        tipo: event.tipo,
                        feriado: event.feriado
                    };
                });

                successCallback(events);  // Pasar los eventos filtrados al calendario
            },
            error: function(xhr, status, error) {
                console.log("Error al obtener los eventos:", error);
                failureCallback();
            }
        });
    },
    eventDidMount: function(info) {
        $(info.el).tooltip({
            title: info.event.title,  // Muestra el título completo al pasar el cursor
            placement: 'top',
            trigger: 'hover',
            container: 'body'
        });
    },
    headerToolbar: {
        left: 'prev,next today',
        center: 'title',
        right: 'dayGridMonth,timeGridWeek,timeGridDay'
    },
    eventClick: function(info) {
        eventId = info.event.id;
        var isFeriado = info.event.extendedProps.feriado;

        if (isFeriado) {
            $('#btnActualizar').hide();
            $('#btnEliminar').hide();
        } else {
            $('#btnActualizar').show();
            $('#btnEliminar').show();
        }

        var inicio_formateado = info.event.start ? formatToYYYYMMDD(info.event.start) : '';
        var fin_formateado = info.event.end ? formatToYYYYMMDD(info.event.end) : '';

        $('#inputTitulo').val(info.event.title);
        $('#inputDescripcion').val(info.event.extendedProps.description);
        $('#datepicker1').val(inicio_formateado);
        $('#datepicker').val(fin_formateado);
        $('#inputTipo').val(info.event.extendedProps.tipo);
    }
});

calendar.render();

// Filtrar eventos cuando se cambie la opción en el select
$('#event-type-filter').change(function() {
    calendar.refetchEvents();  // Recargar los eventos con el filtro aplicado
});



    