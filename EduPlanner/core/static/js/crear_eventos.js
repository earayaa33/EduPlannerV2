document.getElementById('evento-form').addEventListener('submit', async function(event) {
    event.preventDefault();  // Evita el envío tradicional del formulario

    // Obtén los datos del formulario
    const formData = new FormData(this);

    // Convierte los datos del formulario a un objeto
    const formObject = {};
    formData.forEach((value, key) => {
        if (key !== 'csrfmiddlewaretoken') {
        formObject[key] = value;
    }
    });

    if (formObject.fecha_inicio_day && formObject.fecha_inicio_month && formObject.fecha_inicio_year) {
        const fechaInicio = `${formObject.fecha_inicio_year}-${formObject.fecha_inicio_month.padStart(2, '0')}-${formObject.fecha_inicio_day.padStart(2, '0')}`;
        formObject.fecha_inicio = fechaInicio;
        delete formObject.fecha_inicio_day;
        delete formObject.fecha_inicio_month;
        delete formObject.fecha_inicio_year;
    }

    if (formObject.fecha_finalizacion_day && formObject.fecha_finalizacion_month && formObject.fecha_finalizacion_year) {
        const fechaFinalizacion = `${formObject.fecha_finalizacion_year}-${formObject.fecha_finalizacion_month.padStart(2, '0')}-${formObject.fecha_finalizacion_day.padStart(2, '0')}`;
        formObject.fecha_finalizacion = fechaFinalizacion;
        delete formObject.fecha_finalizacion_day;
        delete formObject.fecha_finalizacion_month;
        delete formObject.fecha_finalizacion_year;
    }

    console.log(formObject);

    try {
    // Envia la solicitud POST al API REST
    const response = await fetch('/api/eventos/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',  // Asegúrate de que sea JSON
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value  // Asegúrate de incluir el token CSRF
        },
        body: JSON.stringify(formObject)  // Envía los datos como JSON
    });

    const data = await response.json();
    
    if (response.ok) {
        alert('Evento creado con éxito');
        window.location.href = "{% url 'Panel Admin' %}";  // Redirige a la página de administración
    } else {
        alert('Error al crear el evento: ' + data.detail);
    }
    } catch (error) {
        console.error('Error:', error);
        alert('Ocurrió un error al enviar los datos.');
    }
    });


var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',  // Vista inicial del calendario (mes)
        locale: 'es',  // Configurar el idioma en español
        events: function(fetchInfo, successCallback, failureCallback) {
                $.ajax({
                    url: '/api/eventos-y-feriados/',  // URL de la API para obtener los eventos
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