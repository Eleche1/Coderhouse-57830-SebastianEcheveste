from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Cliente, Cancha, Reserva
from datetime import timedelta, datetime, time

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

class CanchaForm(forms.ModelForm):
    class Meta:
        model = Cancha
        fields = '__all__'

class ReservaForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(), 
        empty_label="Seleccione un cliente"
    )

    # Generar opciones de duración en múltiplos de 30 minutos
    DURACION_OPCIONES = [
        (timedelta(hours=0, minutes=30), '30 minutos'),
        (timedelta(hours=1), '1 hora'),
        (timedelta(hours=1, minutes=30), '1 hora 30 minutos'),
        (timedelta(hours=2), '2 horas'),
    ]

    duracion = forms.ChoiceField(choices=DURACION_OPCIONES)
    
    # Generar opciones de hora de inicio en intervalos de 30 minutos
    HORA_INICIO_OPCIONES = [(time(hour=h, minute=m), f"{h:02}:{m:02}") 
                            for h in range(9, 24)  # Horas entre 9 AM (9) y 11 PM (23)
                            for m in (0, 30)]  # Múltiplos de 30 minutos

    hora_inicio = forms.ChoiceField(choices=HORA_INICIO_OPCIONES)

    class Meta:
        model = Reserva
        fields = '__all__'
        widgets = {
            "fecha_reserva": forms.DateInput(attrs={
                "type": "date",
                "min": datetime.now().date().isoformat()  # Solo permite fechas desde hoy
            }),
        }

    def clean(self):

        cleaned_data = super().clean()
        fecha_reserva = cleaned_data.get('fecha_reserva')
        hora_inicio = cleaned_data.get('hora_inicio')

        if fecha_reserva and hora_inicio:
            # Obtener la fecha y hora actual
            now = datetime.now()
            # Convertir la hora_inicio de cadena a objeto time
            hora_inicio_time = time.fromisoformat(hora_inicio)  # Convierte la cadena en objeto time
            selected_datetime = datetime.combine(fecha_reserva, hora_inicio_time)

            # Validar que la fecha y hora seleccionadas no sean anteriores a la actual
            if selected_datetime < now:
                raise forms.ValidationError("La fecha y hora seleccionadas no pueden ser anteriores a la fecha y hora actuales.")

        return cleaned_data
    
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')