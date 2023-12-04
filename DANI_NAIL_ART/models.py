from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    user_id = models.CharField(max_length=10, unique=True, default=uuid.uuid4)
    es_administrador = models.BooleanField(default=False)


    def __str__(self):
        return self.username

class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)
    disponibilidad = models.BooleanField()
    precio = models.DecimalField(max_digits=10, decimal_places=3, validators=[MinValueValidator(0)])
    imagen = models.ImageField(default='default_image.jpg')

    def __str__(self):
        return self.nombre

class Cita(models.Model):
    nombre = models.CharField(max_length=100, null=True, blank=True)
    descripcion = models.CharField(max_length=100, null=True, blank=True)
    precio = models.CharField(max_length=100, null=True, blank=True)
    fecha = models.DateField()
    hora = models.TimeField()
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.nombre

class Promociones(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)
    disponibilidad = models.BooleanField()
    precio = models.DecimalField(max_digits=10, decimal_places=3, validators=[MinValueValidator(0)])
    imagen = models.ImageField()

    def __str__(self):
        return self.nombre

class Galeria(models.Model):
    imagen = models.ImageField(upload_to='galeria/')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.imagen.name

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name
