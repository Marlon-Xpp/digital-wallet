from django.shortcuts import render

# Create your views here.
# Enviar Dinero
# Solicitar Dinero
# Historial de trasacciones
# Código QR para Enviar/Recibir (marlon)

def send_receive(request):
    
    return render(request, "send_receive.html")


