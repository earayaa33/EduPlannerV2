from django.db import models

# Create your models here.

class Evento(models.Model):

    TIPO_EVENTO = [
        ('inicio de semestre', 'Inicio de semestre'),
        ('fin de Semestre', 'Fin de Semestre'),
        ('inicio de Inscripción de Asignaturas','Inicio de Inscripción de Asignaturas'),
        ('fin de Inscripción de Asignaturas','Fin de Inscripción de Asignaturas'),
        ('receso Académico','Receso Académico'),
        ('feriado Nacional', 'Feriado Nacional'),
        ('feriado Regional','Feriado Regional'),
        ('inicio de Plazos de Solicitudes Administrativas','Inicio de Plazos de Solicitudes Administrativas'),
        ('fin de Plazos de Solicitudes Administrativas','Fin de Plazos de Solicitudes Administrativas'),
        ('inicio de Plazos para la Gestión de Beneficios','Inicio de Plazos para la Gestión de Beneficios'),
        ('fin de Plazos para la Gestión de Beneficios','Fin de Plazos para la Gestión de Beneficios'),
        ('ceremonia de Titulación o Graduación','Ceremonia de Titulación o Graduación'),
        ('reunión de Consejo Académico','Reunión de Consejo Académico'),
        ('talleres y Charlas','Talleres y Charlas'),
        ('día de Orientación para Nuevos Estudiantes','Día de Orientación para Nuevos Estudiantes'),
        ('eventos Extracurriculares','Eventos Extracurriculares'),
        ('inicio de Clases', 'Inicio de Clases'),
        ('ultimo Día de Clases','Último Día de Clases'),
        ('día de Puertas Abiertas','Día de Puertas Abiertas'),
        ('suspensión de Actividades Completa','Suspensión de Actividades Completa'),
        ('suspensión de Actividades Parcial','Suspensión de Actividades Parcial')
    ]

    titulo = models.CharField(max_length=200)  
    descripcion = models.TextField()          
    fecha_inicio = models.DateTimeField()     
    fecha_finalizacion = models.DateTimeField()  
    tipo = models.CharField(max_length=100, choices=TIPO_EVENTO)  

    def __str__(self):
        return self.titulo  