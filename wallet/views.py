from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

#AQUI VA LA LOGICA  DE LA APLICACION WALLET

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

