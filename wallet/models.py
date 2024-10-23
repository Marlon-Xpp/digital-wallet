from django.db import models
from decimal import Decimal
from user_auth import models as md
from django.dispatch import receiver
from django.db.models.signals import post_save

class Wallet(models.Model):
    user = models.OneToOneField(md.CustomUser, on_delete=models.CASCADE)  # Relación uno a uno con el usuario
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Saldo de la billetera
    currency = models.CharField(max_length=3, default='PEN')  # Moneda de la billetera
    status = models.CharField(max_length=20, default='active')  # Estado de la billetera
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación
    updated_at = models.DateTimeField(auto_now=True)  # Fecha de última actualización

    #codigo QR    
    def __str__(self):
        return f'Wallet for {self.user.username} - Balance: {self.balance} {self.currency}'
    def get_balance(self):
        return self.balance
    
    def get_status(self):
        return self.status
    
    def deposit(self, amount):
        self.balance += amount
        self.save()

    # Método para agregar fondos
    def add_funds(self, amount):
        if amount > 0:
            self.balance += Decimal(amount)
            self.save()
        else:
            raise ValueError("El monto debe ser positivo.")
    
    def transference_funds(self, amount):
        if amount > 0:
            self.balance -= Decimal(amount)
            self.save()

    # Método para retirar fondos
    def withdraw_funds(self, amount):
        if amount > 0:
            if self.balance >= amount:
                self.balance -= amount
                self.save()
            else:
                raise ValueError("Fondos insuficientes.")
        else:
            raise ValueError("El monto debe ser positivo.")

    # Método para comprobar si la billetera está activa
    def is_active(self):
        return self.status == 'active'

    # Método para desactivar la billetera
    def desactivate(self):
        self.status = 'inactive'
        self.save()


class UserPayment(models.Model):
    id_wallet = models.ForeignKey(Wallet,on_delete=models.CASCADE)
    payment_bool = models.BooleanField(default=False)
    stripe_checkout_id = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación

    def getStripe_checkout_id(self):
        return self.stripe_checkout_id

    def __str__(self) -> str:
        return f"Billetera {self.id_wallet} - id de stripe {self.stripe_checkout_id}"














#user_Car real

#user_car virtual
#estandar de asociar tarjetas, encriptados




#user_Care retiro;
#numero usuario
#nombre
#descripcion
#actividad
#payment
#deposit
#fecha
#billetera - un iq qr

#campo numero ya existe:  codigo postal pais
#ingles

