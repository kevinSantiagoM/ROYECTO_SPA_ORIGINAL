#-----------------Inicio de secion

# forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Nombre de Usuario')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=10 ,label='Número Telefónico')
    email = forms.EmailField(label='Correo Electrónico')
    username = forms.CharField(label='Nombre de Usuario')
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Verificar Contraseña', widget=forms.PasswordInput)
    es_administrador = forms.BooleanField(label='¿Registrarse como administrador?', required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password1', 'password2', 'es_administrador']



from django import forms
from .models import Servicio, Promociones, Galeria
from .models import Cita

#---------------CREAR CITAS------------------------------------

from django import forms
from .models import Servicio, Promociones, Galeria
from .models import Cita

#---------------CREAR CITAS------------------------------------

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['nombre', 'descripcion', 'precio', 'fecha', 'hora']

        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.Select(attrs={'class': 'custom-select'}),
            'nombre': forms.TextInput(attrs={'readonly': 'readonly'}),
            'descripcion': forms.TextInput(attrs={'readonly': 'readonly'}),
            'precio': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Definir las opciones de hora permitidas
        horas_permitidas = [
            ('07:00', '7:00 AM'),
            ('09:00', '9:00 AM'),
            ('11:00', '11:00 AM'),
            ('13:00', '1:00 PM'),
            ('15:00', '3:00 PM'),
            ('17:00', '5:00 PM'),
            ('19:00', '7:00 PM'),
        ]

        # Establecer las opciones de hora en el campo de hora
        self.fields['hora'].widget.choices = horas_permitidas

    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora')

        if fecha and hora:
            cita_datetime = datetime.combine(fecha, hora)
            cita_datetime_aware = timezone.make_aware(cita_datetime, timezone.get_current_timezone())

            if cita_datetime_aware < timezone.now():
                raise ValidationError('La fecha y hora no pueden ser anteriores a la fecha y hora actuales.')

        return cleaned_data


#-----------------AGREGAR SERVICIOS-----------------------------
class Agendar_Servicio(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['nombre', 'descripcion', 'disponibilidad', 'precio', 'imagen']

#-----------------AGREGAR PROMOCIONES
class Agendar_PromocionesForm(forms.ModelForm):
    class Meta:
        model = Promociones
        fields = ['nombre', 'descripcion', 'disponibilidad', 'precio', 'imagen']

#---------------AGREGAR IMAGENES------------------------
class Agendar_Galeria(forms.ModelForm):

    class Meta: 
        model = Galeria
        fields = ['imagen']


#---------------CREAR CITAS DE PROMOCION------------------------------------

# forms.py

from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']


