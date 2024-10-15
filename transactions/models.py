from django.db import models
#from share import models as ShareMD
from django.utils.module_loading import import_string
from wallet.models import Wallet

#def Wallet():
    #get_instance = ShareMD.get_instance_Wallet()  # Importación dinámica
    #instancia = get_instance()
    #return instancia
#    pass

class Transference(models.Model):
    "solo lo ve el usuario : username , monto , tipo "  
    "solo la base de datos : nombre apellido , username, monto, tipo , estado "

    TRANSFERENCE_CHOICES = [
        ('SEND', 'send'),
        ('RELOAD', 'reload'),
        ('REQUEST', 'request'),

    ]
    idWallet = models.ForeignKey( Wallet(),on_delete=models.CASCADE)

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
