//Funcion para formatear las fechas

function formatToYYYYMMDD(date) {
    var d = new Date(date);
    var year = d.getFullYear();
    var month = ('0' + (d.getMonth() + 1)).slice(-2);  // Añadir 1 ya que los meses son de 0 a 11
    var day = ('0' + d.getDate()).slice(-2);  
    return year + '-' + month + '-' + day;  
}

// Función para limpiar el formulario después de eliminar un evento
function limpiarFormulario() {
    $('#inputTitulo').val('');
    $('#inputDescripcion').val('');
    $('#datepicker1').val('');
    $('#datepicker').val('');
    $('#inputTipo').val('');
    eventId = null; // Resetear el id del evento seleccionado
}




var eventId = null;  // Variable global para almacenar el id del evento seleccionado

var calendarEl = document.getElementById('calendar');
var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',  // Vista inicial del calendario (mes)
    locale: 'es',  // Configurar el idioma en español
    events: function(fetchInfo, successCallback, failureCallback) {
        $.ajax({
            url: '/api/eventos/',  // URL de la API para obtener los eventos
            method: 'GET',
            success: function(data) {
                var eventos = data.map(function(evento) {
                    return {
                        id: evento.id,  
                        title: evento.titulo,  
                        start: evento.fecha_inicio,  
                        end: evento.fecha_finalizacion, 
                        description: evento.descripcion,
                        tipo: evento.tipo
                    };
                });
                successCallback(eventos);  
            },
            error: function(xhr, status, error) {
                console.log("Error al obtener los eventos:", error);
                failureCallback();  
            }
        });
    },
    headerToolbar: {
        left: 'prev,next today',  
        center: 'title',  
        right: 'dayGridMonth,timeGridWeek,timeGridDay'  
    },
    eventClick: function(info) {
        var inicio_formateado= info.event.start ? formatToYYYYMMDD(info.event.start) : '';
        var fin_formateado = info.event.end ? formatToYYYYMMDD(info.event.end) : '';
        
        eventId = info.evento.id;  
        $('#inputTitulo').val(info.evento.title);
        $('#inputDescripcion').val(info.evento.extendedProps.description);
        $('#datepicker1').val(inicio_formateado);
        $('#datepicker').val(fin_formateado);
        $('#inputTipo').val(info.evento.extendedProps.tipo);
    }
});

calendar.render();  


//Para enviar los datos modificados
$('#btnActualizar').click(function(e) {
    e.preventDefault();  // Prevenir el comportamiento predeterminado del formulario

    if (eventId !== null) {
        // Recoger los valores del formulario
        var titulo = $('#inputTitulo').val();
        var descripcion = $('#inputDescripcion').val();
        var tipo = $('#inputTipo').val();
        var fecha_inicio = $('#datepicker1').val();
        var fecha_finalizacion = $('#datepicker').val();

        var fecha_inicio_formatted = formatToYYYYMMDD(fecha_inicio);
        var fecha_finalizacion_formatted = formatToYYYYMMDD(fecha_finalizacion);


        // Crear un objeto con los nuevos datos del evento
        var updatedEvent = {
            titulo: titulo,
            descripcion: descripcion,
            tipo: tipo,
            fecha_inicio: fecha_inicio,
            fecha_finalizacion: fecha_finalizacion
        };

        console.log(updatedEvent);

        // Enviar la solicitud PUT al backend
        $.ajax({
            url: '/api/eventos/' + eventId + '/',  // URL de la API para actualizar el evento (usando el id del evento)
            method: 'PUT',  // Método PUT para actualizar
            data: JSON.stringify(updatedEvent),  // Datos del evento actualizado
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken  // Incluir el token CSRF en los encabezados
            },
            success: function(response) {
                alert('Evento actualizado con éxito');
                calendar.refetchEvents();  // Recargar los eventos en el calendario
            },
            error: function(xhr, status, error) {
                console.log('Error al actualizar el evento:', error);
            }
        });
    } else {
        alert('Por favor, selecciona un evento para modificar');
    }
});

//Eliminar un evento

$('#btnEliminar').click(function (e) {
    e.preventDefault(); // Prevenir comportamiento predeterminado del botón

    if (eventId !== null) { // Verificar que un evento esté seleccionado
        // Mostrar un cuadro de confirmación al usuario
        if (confirm('¿Estás seguro de que deseas eliminar este evento? Esta acción no se puede deshacer.')) {
            // Enviar la solicitud DELETE al backend
            $.ajax({
                url: '/api/eventos/' + eventId + '/', // URL de la API para eliminar el evento
                method: 'DELETE', // Método DELETE para eliminar
                headers: {
                    'X-CSRFToken': csrfToken // Token CSRF para autenticación
                },
                success: function (response) {
                    alert('Evento eliminado con éxito');
                    calendar.refetchEvents(); // Recargar los eventos en el calendario
                    limpiarFormulario(); // Limpiar los campos del formulario
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
