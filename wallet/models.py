from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from user_auth import models as md
    
#class User(models.Model):
    #name = models.CharField(max_length=255)
    #lastname = models.CharField(max_length=255)
    #tenma de seguridad !los nombres y apellidos al hacer la transferencia
    #username = models.CharField(max_length=150, unique=True)  # Nombre de usuario único
    #email = models.EmailField(unique=True)  # Correo único
    #hone_number = models.CharField(max_length=10, blank=True, null=True)

    #def __str__(self):
    #    return self.username
    
    
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
    
    def deposit(self, amount):
        self.balance += amount
        self.save()

    # Método para agregar fondos
    def add_funds(self, amount):
        if amount > 0:
            self.balance += amount
            self.save()
        else:
            raise ValueError("El monto debe ser positivo.")

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





    
class PaymentMethod(models.Model):
    description = models.CharField(max_length=250, default="")
    payment = models.OneToOneField(Wallet, on_delete=models.CASCADE)
    MethodName = models.CharField(max_length=100,default= "YAPE")
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación



    def __str__(self):
        return f'Method: {self.MethodName} for Wallet {self.payment.user.username}'

    # Método para cambiar el método de pago
    def change_method(self, new_method_name):
        self.MethodName = new_method_name
        self.save()
    

class Transference(models.Model):
    TRANSFERENCE_CHOICES = [
        ('SEND', 'send'),
        ('REQUEST', 'request'),
    ]
    idWallet = models.ForeignKey(Wallet,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 
    type_transference = models.CharField(max_length=100, choices= TRANSFERENCE_CHOICES)

    def __str__(self):
        return f'Transference: {self.get_type_transference_display()} - Amount: {self.amount}'

    # Método para realizar una transferencia
    def execute_transference(self, target_wallet):
        if self.type_transference == 'SEND':
            # Verifica si la billetera tiene fondos suficientes
            if self.idWallet.balance >= self.amount:
                self.idWallet.withdraw_funds(self.amount)
                target_wallet.add_funds(self.amount)
            else:
                raise ValueError("Fondos insuficientes en la billetera de origen.")
        elif self.type_transference == 'REQUEST':
            # Se podría implementar la lógica de solicitud aquí
            pass
        
    #def history_transference(self, target_wallet):
        #



#class Account(models.Model):
#    balance = models.FloatField(default=0.00)#

#    def __str__(self):
#        return 'Account: %s' % self.payment.user.username

#    def get_update_url(self):
#        return reverse('account_transfer', kwargs={'pk': self.pk})

#    def save(self, *args, **kwargs):
#        # ensure that the database only stores 2 decimal places
#        self.balance = round(self.balance, 2)
#        super(Account, self).save(*args, **kwargs)

#da quen envcio

#monto
#nombre de quien envio

#numero usuario
#nombre
#descripcion




#actividad
#payment
#deposit


#fecha
#hora mundial - hora zonal

# settings - cambiar hora de zona 


#los 3 utlimos numeros del telefono

#billetera - un iq qr




# numero indicar pais . : no ingresar letras y solo numeros : Tamaño de numero de acuerdo al indicador de pais
#numero de celular



#campo numero ya existe:  codigo postal pais
#ingles

