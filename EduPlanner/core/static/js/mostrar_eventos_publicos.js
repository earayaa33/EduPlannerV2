var calendarEl = document.getElementById('calendar');
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