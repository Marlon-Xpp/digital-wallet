from django.shortcuts import render
from .models import User

# Create your views here.

#AQUI VA LA LOGICA  DE LA APLICACION WALLET

#Gestion del saldo
class Account():
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
            
            Users = User.objects.get(username = name)
            
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