document.getElementById('evento-form').addEventListener('submit', async function(event) {
    event.preventDefault();  

    
    const formData = new FormData(this);

    
    const formObject = {};
    formData.forEach((value, key) => {
        if (key !== 'csrfmiddlewaretoken') {
        formObject[key] = value;
    }
    });

    const esOficial = document.getElementById('checkOficial').checked;
    formObject.es_oficial = esOficial;

    const esInterno = document.getElementById('checkPlanificacion').checked;
    formObject.planificacion_interna = esInterno

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
    
    const response = await fetch('/api/eventos/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',  
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value  
        },
        body: JSON.stringify(formObject)  
    });

    const data = await response.json();
    
    if (response.ok) {
        alert('Evento creado con éxito');
        window.location.href = '';  
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
        initialView: 'dayGridMonth',  
        locale: 'es',  
        events: function(fetchInfo, successCallback, failureCallback) {
                $.ajax({
                    url: '/api/eventos-y-feriados/',  
                    method: 'GET',
                    success: function(data) {
                        var events = data.map(function(event) {
                            return {
                                title: event.titulo,  
                                start: event.fecha_inicio,  
                                end: event.fecha_finalizacion  
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