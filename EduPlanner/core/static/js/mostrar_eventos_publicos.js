
var tipoSeleccionado = '';

var calendarEl = document.getElementById('calendar');
var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',  
    locale: 'es',  
    events: function(fetchInfo, successCallback, failureCallback) {
            
            
        var url = '/api/eventos-publicos-y-feriados/';
            
         $.ajax({
            url: url,  
            method: 'GET',
            success: function(data) {
                
                var events = data.map(function(event) {
                    return {
                        title: event.titulo,  
                        start: event.fecha_inicio,  
                        end: event.fecha_finalizacion,  
                        description: event.descripcion,
                        tipo: event.tipo,
                        feriado: event.feriado
                    };
                });
                successCallback(events);  
            },
            error: function(xhr, status, error) {
                console.log("Error al obtener los eventos:", error);
                failureCallback();  
            }
        });
    },
    eventDidMount: function(info) {
        $(info.el).tooltip({
            title: info.event.title,  
            placement: 'top',
            trigger: 'hover',
            container: 'body'
        });
    },
        headerToolbar: {
            left: 'prev,next today',  
            center: 'title',  
            right: 'dayGridMonth,timeGridWeek,timeGridDay'  
        }
    });

calendar.render();  

$(document).ready(function() {
    let tipoSeleccionado = ''; 

    function cargarEventos(tipo) {
        console.log('Tipo de evento seleccionado:', tipo);
        
        let url = '/api/eventos-publicos-y-feriados/';
    
        
        if (tipo) {
            url += '?tipo=' + tipo;
        }
    
        
        $.get(url, function(data) {
            console.log("Respuesta de la API:", data);
            
            var events = calendar.getEvents();  

            
            events.forEach(function(event) {
                event.remove();  
            });

            
            data.forEach(function(evento) {
                
                let eventExists = calendar.getEvents().some(function(existingEvent) {
                    return existingEvent.startStr === evento.fecha_inicio && existingEvent.title === evento.titulo;
                });

                
                if (!eventExists) {
                    calendar.addEvent({
                        title: evento.titulo,
                        start: evento.fecha_inicio,
                        end: evento.fecha_finalizacion, 
                        description: evento.descripcion,
                        type: evento.tipo,
                        allDay: true 
                    });
                }
            });
        });
    }
    
    
    $('#event-type-filter').on('change', function() {
        tipoSeleccionado = $(this).val(); 
        cargarEventos(tipoSeleccionado); 
    });
    
    
    calendar.on('datesSet', function() {
        cargarEventos(tipoSeleccionado); 
    });

    
    cargarEventos(tipoSeleccionado);
});
