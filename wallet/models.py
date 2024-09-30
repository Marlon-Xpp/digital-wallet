from django.db import models
from decimal import Decimal
from user_auth import models as md


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
    "solo lo ve el usuario : username , monto , tipo "  
    "solo la base de datos : nombre apellido , username, monto, tipo , estado "

    TRANSFERENCE_CHOICES = [
        ('SEND', 'send'),
        ('REQUEST', 'request'),
    ]
    idWallet = models.ForeignKey(Wallet,on_delete=models.CASCADE)

    name = models.CharField(max_length=250,null=False,blank=False)
    lastname = models.CharField(max_length=250,null=False,blank=False)
    phone = models.CharField(max_length=15, blank=True, null=True)
    username = models.CharField(max_length=250, null=False, blank=False)

    description = models.CharField(max_length=250, default="")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 
    type_transference = models.CharField(max_length=100, choices= TRANSFERENCE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación

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

