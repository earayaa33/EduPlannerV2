var calendarEl = document.getElementById('calendar');
var tipoSeleccionado = '';

var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',  // Vista inicial del calendario (mes)
        locale: 'es',  // Configurar el idioma en español
        events: function(fetchInfo, successCallback, failureCallback) {
                $.ajax({
                    url: '/api/eventos-publicos-y-feriados/',  // URL de la API para obtener los eventos
                    method: 'GET',
                    success: function(data) {
                        var events = data.map(function(event) {
                            return {
                                title: event.titulo,  // Título del evento
                                start: event.fecha_inicio,  // Fecha de inicio
                                end: event.fecha_finalizacion  // Fecha de finalización
                            };
                        });
                        successCallback(events);  // Retornar los eventos al calendario
                    },
                    error: function(xhr, status, error) {
                        console.log("Error al obtener los eventos:", error);
                        failureCallback();  // Si ocurre un error, notificar
                    }
                });
            },
            headerToolbar: {
                left: 'prev,next today',  // Botones para cambiar de mes
                center: 'title',  // Título del mes actual
                right: 'dayGridMonth,timeGridWeek,timeGridDay'  // Opciones para cambiar la vista
            }
        });

calendar.render();  // Renderizar el calendario    

$(document).ready(function() {
    let tipoSeleccionado = ''; 

    function cargarEventos(tipo) {
        console.log('Tipo de evento seleccionado:', tipo);
        // URL de la API de eventos públicos y feriados
        let url = '/api/eventos-publicos-y-feriados/';
    
        // Si se selecciona un tipo de evento, agregarlo como parámetro de consulta (query parameter)
        if (tipo) {
            url += '?tipo=' + tipo;
        }
    
        // Hacer la solicitud AJAX
        $.get(url, function(data) {
            console.log("Respuesta de la API:", data);
            // Obtener los eventos actuales en el calendario
            var events = calendar.getEvents();  

            // Eliminar todos los eventos en el calendario antes de agregar los nuevos
            events.forEach(function(event) {
                event.remove();  // Eliminar cada evento
            });

            // Agregar los nuevos eventos, asegurándose de no duplicarlos
            data.forEach(function(evento) {
                // Verificar si el evento ya existe en el calendario
                let eventExists = calendar.getEvents().some(function(existingEvent) {
                    return existingEvent.startStr === evento.fecha_inicio && existingEvent.title === evento.titulo;
                });

                // Si el evento no existe, agregarlo
                if (!eventExists) {
                    calendar.addEvent({
                        title: evento.titulo,
                        start: evento.fecha_inicio,
                        end: evento.fecha_finalizacion, // Si existe
                        description: evento.descripcion,
                        type: evento.tipo,
                        allDay: true // Puedes ajustar esto si no es todo el día
                    });
                }
            });
        });
    }
    
    // Al cambiar el filtro, recargar los eventos
    $('#event-type-filter').on('change', function() {
        tipoSeleccionado = $(this).val(); // Obtener el valor seleccionado del filtro
        cargarEventos(tipoSeleccionado); // Llamar a la función para cargar los eventos
    });
    
    // Recargar los eventos al cambiar de mes o vista (y mantener el filtro seleccionado)
    calendar.on('datesSet', function() {
        cargarEventos(tipoSeleccionado); // Usar el tipoSeleccionado actual
    });

    // Cargar todos los eventos por defecto al cargar la página
    cargarEventos(tipoSeleccionado);
});
