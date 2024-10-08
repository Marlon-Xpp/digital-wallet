from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser



# Create your models here.
class CustomUser(AbstractUser):
    # Número de teléfono
    phone = models.CharField(max_length=15, blank=True, null=True)
    # Código del país
    country_code = models.CharField(max_length=4, blank=True, null=True)
    
    # -------------------FALTA CORREGIR ESTE CODIGO -------------------
    # Código QR
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    # Clave de encriptación
    encryption_key = models.BinaryField(blank=True, null=True)

    def __str__(self):
        return self.username
    
class LoginAttempt(models.Model):
    username = models.CharField(max_length=10)
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.username} - {self.ip_address} - {self.timestamp}"
    
# crearn un modelo para el campo codigo postal  