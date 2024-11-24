

function formatToYYYYMMDD(date) {
    var d = new Date(date);
    var year = d.getFullYear();
    var month = ('0' + (d.getMonth() + 1)).slice(-2);  
    var day = ('0' + d.getDate()).slice(-2);  
    return year + '-' + month + '-' + day;  
}



var eventId = null;  

var calendarEl = document.getElementById('calendar');
var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',  
    locale: 'es',  
    events: function(fetchInfo, successCallback, failureCallback) {
        $.ajax({
            url: '/api/eventos-y-feriados/',  
            method: 'GET',
            success: function(data) {
                var events = data.map(function(event) {
                    return {
                        id: event.id,  
                        title: event.titulo,  
                        start: event.fecha_inicio,  
                        end: event.fecha_finalizacion , 
                        description: event.descripcion,
                        tipo: event.tipo,
                        feriado : event.feriado
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
    },
    eventClick: function(info) {

         
         eventId = info.event.id;
         
         var isFeriado = info.event.extendedProps.feriado;
 
         
         if (isFeriado) {
             $('#btnActualizar').hide();  
             $('#btnEliminar').hide();
         } else if(!isFeriado) {
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



$('#btnActualizar').click(function(e) {
    e.preventDefault();  

    if (eventId !== null) {
        
        var titulo = $('#inputTitulo').val();
        var descripcion = $('#inputDescripcion').val();
        var tipo = $('#inputTipo').val();
        var fecha_inicio = $('#datepicker1').val();
        var fecha_finalizacion = $('#datepicker').val();

        var fecha_inicio_formatted = formatToYYYYMMDD(fecha_inicio);
        var fecha_finalizacion_formatted = formatToYYYYMMDD(fecha_finalizacion);


        
        var updatedEvent = {
            id : eventId,
            titulo: titulo,
            descripcion: descripcion,
            tipo: tipo,
            fecha_inicio: fecha_inicio,
            fecha_finalizacion: fecha_finalizacion
        };

        console.log(updatedEvent);

        
        $.ajax({
            url: '/api/eventos/' + eventId + '/',  
            method: 'PUT',  
            data: JSON.stringify(updatedEvent),  
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken  
            },
            success: function(response) {
                alert('Evento actualizado con éxito');
                calendar.refetchEvents();  
            },
            error: function(xhr, status, error) {
                const errorMessage = xhr.responseJSON && xhr.responseJSON.detail ? xhr.responseJSON.detail : "Error desconocido";
                alert("Error: " + errorMessage);
            }
        });
    } else {
        alert('Por favor, selecciona un evento para modificar');
    }
});



$('#btnEliminar').click(function (e) {
    e.preventDefault(); 

    if (eventId !== null) { 
        
        if (confirm('¿Estás seguro de que deseas eliminar este evento? Esta acción no se puede deshacer.')) {
            
            $.ajax({
                url: '/api/eventos/' + eventId + '/', 
                method: 'DELETE', 
                headers: {
                    'X-CSRFToken': csrfToken 
                },
                success: function (response) {
                    alert('Evento eliminado con éxito');
                    calendar.refetchEvents(); 
                    limpiarFormulario(); 
                },
                error: function (xhr, status, error) {
                    console.log('Error al eliminar el evento:', error);
                    alert('No se pudo eliminar el evento. Por favor, intenta de nuevo.');
                }
            });
        }
    } else {
        alert('Por favor, selecciona un evento para eliminar.');
    }
});


function limpiarFormulario() {
    $('#inputTitulo').val('');
    $('#inputDescripcion').val('');
    $('#datepicker1').val('');
    $('#datepicker').val('');
    $('#inputTipo').val('');
    eventId = null; 
}

