from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from wallet.models import Wallet ,Transference
from django.core.exceptions import ObjectDoesNotExist
from share import models as ShareMD

# Create your views here.

#AQUI VA LA LOGICA  DE LA APLICACION WALLET

#Gestion del saldo
class Account():
    

    @login_required
    def __init__(self):
        self.user = ""
        


    def first_wallet(user):
    
        wallet = Wallet(user = user)
        wallet.save()

        return True

    def new_wallet_create(request):
        if request.method == "POST":
            currency = request.POST.get('currency')  # Obtener la moneda del formulario
          #  user_instance = connectionModel.user_instance(request.user.username) # Cambia por el nombre de usuario adecuado
          #  wallet = models.Wallet(user = user_instance,currency=currency)
         #  wallet.save()
        return render(request,"wallet.html",{})
        
   # def change_type_cell    

    def recharge_sldo():
        pass
    
    
    #Informacion sobre la Wallet
    def PersonWallet(request):
    # Obtener el usuario actual
        usuario_actual = request.user
    
        # Filtrar las wallets que pertenecen al usuario actual
        wallet_currency = Wallet.objects.filter(user=usuario_actual)
        

        return render(request,'wallet.html',{'wallet_currency' : wallet_currency })

    #Informacion sobre el balance
    def ViewBalance(Request):
        data= {"Nuevo": "hola"}

        return render(Request,'viewBalance.html',data)
        pass


#Envío de dinero:

class Send(Account):
    
    def __init__(self,):
        pass

    
    #Busca al usuario
    def getQueryUsername(self,):
        
        pass
    

    #Metodo para verificar si el usuario existe, no puede ser el mismo usuario
    @classmethod
    def VerifyUser(cls,usernameUser, requestuser):
        #username = ShareMD.user_query(username=usernameUser,"get_query_username")
        #print(username)
        try:
             if requestuser != usernameUser:
                user = ShareMD.user_query(usernameUser,"get_exits_user")
                return user
            
        except: 
            print("EL USUARIO NO EXISTE")
            return False
    
    @classmethod       
    def VerifyAmount(cls, user , amount):
        try:
            balance = Wallet.objects.get(user=user)
            print(balance)
            
            if balance.get_balance() > 0 and balance.get_balance() >= amount :
                print("Monto suficiente")
                return True
            else :
                print("no hay saldo sufiente")
                return False
        except:
            print("Error al ejecutar")
            return False


    def sendUser(request):
        if request.method == 'POST':
            
            usernameUser = request.POST.get("username","").strip()
            send_money = float(request.POST.get("send_money","").strip())


            if Send.VerifyUser(usernameUser,request.user.username) and Send.VerifyAmount(request.user,send_money):

                try:
                
                    user_wallet_send = ShareMD.user_query(usernameUser,"get_query_username")
                    print(user_wallet_send)
                    wallet_send = Wallet.objects.get(user=user_wallet_send)
                    wallet_user = Wallet.objects.get(user=request.user)
                    print(wallet_send)

                    #Funcion de deposito
                    Transference.objects.create(
                        idWallet=wallet_user,
                        name=request.user.name,
                        lastname=request.user.last_name,
                        phone=request.user.phone,
                        username=request.user.username,
                        amount=send_money,
                        type_transference='SEND'
                    )

                    Transference.objects.create(
                        idWallet=wallet_send,
                        name=user_wallet_send.name,
                        lastname=user_wallet_send.last_name,
                        phone=user_wallet_send.phone,
                        username=user_wallet_send.username,
                        amount=send_money,
                        type_transference='REQUEST'
)

                    print("Deposito realizado")
                except:
                    print("Error al realizar deposito")

                    

        return render(request,'send.html',{})



    def sendMoney(request):
        
        pass

    
    #Obtiene al usuario
    def get_context_data():
        pass



#Send
class SendMoney(Account):
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
class Activity(Account):

    def getHistory(request):
        message = ""
        wallet_user  = Wallet.objects.get(user = request.user)
        try:
            # Usamos filter() en lugar de get() para obtener todas las transferencias
            history_send = Transference.objects.filter(idWallet=wallet_user, type_transference="SEND")
            history_request = Transference.objects.filter(idWallet=wallet_user, type_transference="REQUEST")

            # Si no hay resultados, mostramos el mensaje
            if not history_send.exists() and not history_request.exists():
                message = "No tiene ni una transferencia"

        except Wallet.DoesNotExist:
            message = "No se encontró la billetera del usuario."

       # print(history_request)
        print(history_send)
        return render(request, "activity.html", {
            'history_send': history_send,
            'history_request': history_request,
            'message': message,
            'username': request.user.username,
        })
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

