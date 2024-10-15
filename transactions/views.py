from django.shortcuts import render
import qrcode
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db import transaction
from share import models as ShareMD

from share.models import Wallet, Transference

# Create your views here.
# Enviar Dinero
# Solicitar Dinero
# Historial de trasacciones
# Código QR para Enviar/Recibir (marlon)

# def scan_qr_code():
#     print("se escaneara el cdogio qr")
    
# print("se escaneara el cdogio qr")

def transfer_qr(request):
    return render(request, "transfer_qr.html" )  

# def trantransfer_qr(request, username):
#     # Obtenemos el usuario al que se le va a hacer el pago usando el username
#     user_to_pay = get_object_or_404(CustomUser, username=username)
#     
#     if request.method == "POST":
#         amount = request.POST.get('amount')
#         # Aquí puedes agregar la lógica para realizar la transferencia de dinero
        
#         # Luego de la transferencia puedes redirigir a una página de éxito o dashboard
#         return redirect('success_page')  # Cambiar esto según tu lógica de flujo
    
#     return render(request, "transfer_qr.html", {"user_to_pay": user_to_pay})

    

# from .models import CustomUser


#funciona improtante para mostrar el codigo qr generado

# def send_receive(request):
#     user = request.user  # Obtener el usuario autenticado de la bd
#     qr_code_url = user.qr_code.url if user.qr_code else None  # Obtener la URL del QR si existe
    
#     return render(request, "send_receive.html", {"qr_code_url": qr_code_url})

class Activity():
    @login_required
    @transaction.atomic
    def getHistory(request):
        message = ""
        wallet_user  = Wallet.objects.get(user = request.user)
        try:
            # Usamos filter() en lugar de get() para obtener todas las transferencias
            history_reload = Transference.objects.filter(idWallet=wallet_user, type_transference="reload")
            history_send = Transference.objects.filter(idWallet=wallet_user, type_transference="send"),
            history_request = Transference.objects.filter(idWallet=wallet_user, type_transference="request"),

            # Si no hay resultados, mostramos el mensaje
            #if not history_send.exists() or not history_request.exists():
                #message = "No tiene ni una transferencia"

        except Wallet.DoesNotExist:
            message = "No se encontró la billetera del usuario."

       # print(history_request)
        print(history_send)
        print(history_reload)
        return render(request, "transfer_history.html", {
            'history_send': history_send,
            'history_request': history_request,
            'history_reload': history_reload,
            'message': message,
            'username': request.user.username})
    



    def transfer_widget(request):
        message = ""
        wallet_user  = Wallet.objects.get(user = request.user)
        
        user = request.user  # Obtener el usuario autenticado de la bd
        qr_code_url = user.qr_code.url if user.qr_code else None  # Obtener la URL del QR si existe
        
        try:
            # Usamos filter() en lugar de get() para obtener todas las transferencias
            history_reload = Transference.objects.filter(idWallet=wallet_user, type_transference="RELOAD")
            history_send = Transference.objects.filter(idWallet=wallet_user, type_transference="SEND")
            history_request = Transference.objects.filter(idWallet=wallet_user, type_transference="REQUEST")

            # Si no hay resultados, mostramos el mensaje
            #if not history_send.exists() or not history_request.exists():
                #message = "No tiene ni una transferencia"

        except Wallet.DoesNotExist:
            message = "No se encontró la billetera del usuario."

       # print(history_request)
        print(history_reload)

        print(history_send)
        return render(request, "transfer.html", {
            'history_reload': history_reload,
            'history_request': history_request,
            'history_send': history_send,

            'message': message,
            'username': request.user.username,
            'qr_code_url': qr_code_url
            })




    def NotificationUser(UserSend):
        #Mostrar la ultima transferencia realizada al usuario
        NotifyPush = Transference.objects.get(user=UserSend)



class Send():
    
    def __init__(self,):
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


    @login_required 
    def transfer_send(request):
        
        user = request.user  # Obtener el usuario autenticado de la bd
        qr_code_url = user.qr_code.url if user.qr_code else None  # Obtener la URL del QR si existe
        
        if request.method == 'POST':
            
            usernameUser = request.POST.get("recipient","").strip()
            send_money = float(request.POST.get("amount","").strip())
            message = request.POST.get("message","".strip())

            if Send.VerifyUser(usernameUser,request.user.username) and Send.VerifyAmount(request.user,send_money):
                
                
                try:
                    user_wallet_send = ShareMD.user_query(usernameUser,"get_query_username")
                    print(user_wallet_send)
                    wallet_send = Wallet.objects.get(user=user_wallet_send)
                    wallet_user = Wallet.objects.get(user=request.user)
                    print(wallet_send)

                    wallet_send.add_funds(send_money)
                    
                    wallet_user.transference_funds(send_money)

                    #Funcion de deposito
                    Transference.objects.create(
                        idWallet=wallet_user,
                        name=user_wallet_send.first_name,
                        lastname=user_wallet_send.last_name,
                        phone=user_wallet_send.phone,
                        username=user_wallet_send.username,
                        amount=send_money,
                        type_transference='SEND',
                        description = message

                        )

                    Transference.objects.create(
                        idWallet=wallet_send,

                        name=request.user.first_name,
                        lastname=request.user.last_name,
                        phone=request.user.phone,
                        username=request.user.username,
                        amount=send_money,
                        type_transference='REQUEST',
                        description = message
                        )





                    print("Deposito realizado")
                except:
                    print("Error al realizar deposito")

                    

        return render(request, "transfer_send.html", {"qr_code_url": qr_code_url})




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