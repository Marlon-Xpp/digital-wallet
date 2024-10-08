from django.shortcuts import render
import qrcode

# Create your views here.
# Enviar Dinero
# Solicitar Dinero
# Historial de trasacciones
# Código QR para Enviar/Recibir (marlon)

# def scan_qr_code():
#     print("se escaneara el cdogio qr")

def transfer_qr(request):
    
    return render(request, "transfer_qr.html" )
    

# def trantransfer_qr(request, username):
#     # Obtenemos el usuario al que se le va a hacer el pago usando el username
#     user_to_pay = get_object_or_404(CustomUser, username=username)
    
#     if request.method == "POST":
#         amount = request.POST.get('amount')
#         # Aquí puedes agregar la lógica para realizar la transferencia de dinero
        
#         # Luego de la transferencia puedes redirigir a una página de éxito o dashboard
#         return redirect('success_page')  # Cambiar esto según tu lógica de flujo
    
#     return render(request, "transfer_qr.html", {"user_to_pay": user_to_pay})

    

# from .models import CustomUser

def send_receive(request):
    user = request.user  # Obtener el usuario autenticado de la bd
    qr_code_url = user.qr_code.url if user.qr_code else None  # Obtener la URL del QR si existe
    
    return render(request, "send_receive.html", {"qr_code_url": qr_code_url})



