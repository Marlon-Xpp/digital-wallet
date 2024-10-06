from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import transaction

from share.models import Wallet, Transference
# Create your views here.
# Enviar Dinero
# Solicitar Dinero
# Historial de trasacciones
# Código QR para Enviar/Recibir (marlon)

def send_receive(request):
    
    return render(request, "send_receive.html")


class Activity():
    @login_required
    @transaction.atomic

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

        except wallet.DoesNotExist:
            message = "No se encontró la billetera del usuario."

       # print(history_request)
        print(history_send)
        return render(request, "activity.html", {
            'history_send': history_send,
            'history_request': history_request,
            'message': message,
            'username': request.user.username})
        
    
    def NotificationUser(UserSend):
        #Mostrar la ultima transferencia realizada al usuario
        NotifyPush = Transference.objects.get(user=UserSend)