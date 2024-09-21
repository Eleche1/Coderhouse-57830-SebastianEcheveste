from django.db import models
from django.core.exceptions import ValidationError
from datetime import timedelta, datetime
from decimal import Decimal

class Cliente(models.Model):
    dni = models.CharField(max_length=9)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    celular = models.CharField(max_length=10)
    
    def __str__(self) -> str:
        return f"{self.nombre} {self.apellido} {self.dni} {self.celular}"

class Cancha(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    tipo = models.CharField(max_length=15)
    precio_por_hora = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    disponible = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.nombre} - {self.tipo} - {self.precio_por_hora} - {self.disponible}"

    def cambiar_disponibilidad(self, estado: bool):
        self.disponible = estado
        self.save()

class Reserva(models.Model):
    id = models.BigAutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    cancha = models.ForeignKey(Cancha, on_delete=models.CASCADE)
    fecha_reserva = models.DateField()
    hora_inicio = models.TimeField()
    duracion = models.DurationField(default=timedelta(hours=1))  # Duración de la reserva por defecto 1 hora
    estado = models.CharField(
        max_length=15,
        choices=[('Libre', 'Libre'), ('Reservada', 'Reservada'), ('Cancelada', 'Cancelada')],
        default='Libre'
    )

    def __str__(self) -> str:
        return f"Reserva de {self.cliente.nombre} {self.cliente.apellido} para la cancha {self.cancha.nombre} - {self.cancha.tipo} el {self.fecha_reserva} a las {self.hora_inicio}"
    
    def calcular_precio(self):
        horas = Decimal(self.duracion.total_seconds()) / Decimal(3600)
        if self.cancha.precio_por_hora is None:
            return None
        return self.cancha.precio_por_hora * Decimal(horas)

    def confirmar_reserva(self):
        self.estado = 'Reservada'
        self.save()

    def cancelar_reserva(self):
        self.estado = 'Cancelada'
        self.save()

    def clean(self):
        """ Validación personalizada para evitar reservas en el mismo día y hora en la misma cancha """
        # Obtener las reservas existentes para la misma cancha en el mismo día
        reservas_existentes = Reserva.objects.filter(
            cancha=self.cancha,
            fecha_reserva=self.fecha_reserva
        )
        if self.id is not None:
            reservas_existentes = reservas_existentes.exclude(id=self.id)  # Excluir la reserva actual si se está editando

        # Hora de fin de la reserva actual
        hora_fin = (datetime.combine(self.fecha_reserva, self.hora_inicio) + self.duracion).time()

        # Verificar solapamiento con las reservas existentes
        for reserva in reservas_existentes:
            hora_fin_reserva = (datetime.combine(reserva.fecha_reserva, reserva.hora_inicio) + reserva.duracion).time()

            # Si hay solapamiento entre las horas de inicio y fin
            if (self.hora_inicio < reserva.hora_inicio < hora_fin or
                    self.hora_inicio < hora_fin_reserva < hora_fin or
                    reserva.hora_inicio <= self.hora_inicio < hora_fin_reserva):
                raise ValidationError(f"La cancha {self.cancha.nombre} ya está reservada en este horario.")

    def save(self, *args, **kwargs):
        # Ejecuta la validación personalizada antes de guardar
        self.clean()
        super().save(*args, **kwargs)