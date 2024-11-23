from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from core.models import Evento

class RegistroUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)  
    last_name = forms.CharField(required=True) 
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email = email).exists():
            raise forms.ValidationError('Este correo electronico ya esta registrado')
        return email


class EventoForm(forms.ModelForm):
    titulo = forms.CharField(required=True)
    descripcion = forms.CharField(required=True)
    fecha_inicio = forms.DateField(widget=forms.SelectDateWidget, required=True)  
    fecha_finalizacion = forms.DateField(widget=forms.SelectDateWidget, required=True)  
    tipo = forms.ChoiceField(choices=Evento.TIPO_EVENTO, required=True)
    class Meta:
        model = Evento
        fields = ['titulo', 'descripcion', 'fecha_inicio', 'fecha_finalizacion', 'tipo']