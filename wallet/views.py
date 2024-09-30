from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from wallet import models

# Create your views here.

#AQUI VA LA LOGICA  DE LA APLICACION WALLET

#Gestion del saldo
#Mostrar saldo
#pasarela de pago (marlon)
#recargar dinero
#crear tarjeta virtuales(marlon)


class Account():

    @login_required
    def __init__(self,request):
        self.user = request.user.name
        

    def first_wallet_create(self,currency):
        print(self.user)
    
        #wallet.save()
        return True

    def first_wallet_create(request):
        if request.method == "POST":
            currency = request.POST.get('currency')  # Obtener la moneda del formulario
 
            user_instance = connectionModel.user_instance(request.user.username) # Cambia por el nombre de usuario adecuado
            
            wallet = models.Wallet(user = user_instance,currency=currency)

            wallet.save()

        
        return render(request,"wallet.html",{})
        
   # def change_type_cell    

    def recharge_sldo():
        pass
    
    
    #Informacion sobre la Wallet
    def PersonWallet(Request):
    
        return render(Request,'app/Account.html')

    #Informacion sobre el balance
    def ViewBalance(Request):
        data= {"Nuevo": "hola"}

        return render(Request,'viewBalance  .html',data)
        pass


#Envío de dinero:

class SendSearchUser():
    #Busca al usuario
    def getQueryUsername():
        pass
    #Obtiene al usuario
    def get_context_data():
        pass



#Send
class SendMoney():
    def get_username(self,name):
            pass
            #Users = User.objects.get(username = name)
            
    def form_valid(self, form):
        pass
       # return HttpResponseRedirect(reverse_lazy('send_success'))

class SendSuccess():
    def get(self, request):
        return render(request, 'app/send_success_page.html', {'nbar': 'send'})

class SendError():
    def get(self, request):
        return render(request, '',{'nbar':'error'})
    


#Recepción de dinero:


#Request

#class RequestSearchUser():

    def get_context_data(self, **kwargs):
       pass

#class RequestMoney():

    def get_context_data(self, **kwargs):

        pass
    def form_valid(self, form):


       pass #return HttpResponseRedirect(reverse_lazy('request_success'))


class RequestSuccess():
    def get(self, request):
        pass
        #return render(request, 'app/request_success_page.html', {'nbar': 'request'})


#Recieve
 
class Recieve():

    def get(self):

        pass





#Historial de transacciones:
class Transference():
    #Historial de transferencias Envio
    def HistoryTransferSend():
        pass

    def HistoryTransferRecive():
        pass


#Seguridad de las transacciones:

        
        
#Integraciones con servicios de pago externos (opcional):

class IncompletePayment():

    def get(self, request, pk):
        pass

class IncompletePaymentConfirm():
    
    def get_context_data(self, **kwargs):
        pass

    def form_valid(self, form):
       pass

class PaymentComplete():
    def get(self, request):
        return render(request, 'app/payment_success.html', {'nbar': 'incomplete'})

class IncompleteRequest():
    permission_required = 'app.view_transaction'

    def get(self, request):
        pass
        
class IncompleteRequestDelete():
    #model = Transaction
    #template_name = 'app/request_delete.html'
    #success_url = reverse_lazy('incomplete')
    #permission_required = 'app.delete_transaction'

    def get_context_data(self,):
        pass
    
    

#FUNCIONALIDADES
#Gestión del saldo:
#Envío de dinero:
#Recepción de dinero:
#Historial de transacciones:
#Seguridad de las transacciones:
#Integraciones con servicios de pago externos (opcional):
@login_required
def activity(request):
    return render(request, "activity.html", {"username": request.user.username})

