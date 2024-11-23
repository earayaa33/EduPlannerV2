from django.db import models

# Create your models here.

class Evento(models.Model):

    TIPO_EVENTO = [
        ('inicio_semestre', 'Inicio de Semestre'),
        ('fin_semestre', 'Fin de Semestre'),
        ('inicio_inscripcion_asignaturas', 'Inicio de Inscripción de Asignaturas'),
        ('fin_inscripcion_asignaturas', 'Fin de Inscripción de Asignaturas'),
        ('receso_academico', 'Receso Académico'),
        ('feriado_nacional', 'Feriado Nacional'),
        ('feriado_regional', 'Feriado Regional'),
        ('inicio_plazos_solicitudes', 'Inicio de Plazos de Solicitudes Administrativas'),
        ('fin_plazos_solicitudes', 'Fin de Plazos de Solicitudes Administrativas'),
        ('inicio_plazos_beneficios', 'Inicio de Plazos para la Gestión de Beneficios'),
        ('fin_plazos_beneficios', 'Fin de Plazos para la Gestión de Beneficios'),
        ('ceremonia_titulacion', 'Ceremonia de Titulación o Graduación'),
        ('reunion_consejo', 'Reunión de Consejo Académico'),
        ('talleres_charlas', 'Talleres y Charlas'),
        ('dia_orientacion', 'Día de Orientación para Nuevos Estudiantes'),
        ('eventos_extracurriculares', 'Eventos Extracurriculares'),
        ('inicio_clases', 'Inicio de Clases'),
        ('ultimo_dia_clases', 'Último Día de Clases'),
        ('dia_puertas_abiertas', 'Día de Puertas Abiertas'),
        ('suspension_actividades_completa', 'Suspensión de Actividades Completa'),
        ('suspension_actividades_parcial', 'Suspensión de Actividades Parcial'),
    ]

    titulo = models.CharField(max_length=200)  
    descripcion = models.TextField()          
    fecha_inicio = models.DateTimeField()     
    fecha_finalizacion = models.DateTimeField()  
    tipo = models.CharField(max_length=100, choices=TIPO_EVENTO)  

    def __str__(self):
        return self.titulo  