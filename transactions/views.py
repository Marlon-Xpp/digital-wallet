from django.shortcuts import render , redirect
import qrcode
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db import transaction
from share import models as ShareMD

from share.models import Wallet, Transference

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle

from django.http import HttpResponse


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
        pass
    



    def transfer_widget(request):
        message = ""
        wallet_user  = Wallet.objects.get(user = request.user)

        user = request.user  # Obtener el usuario autenticado de la bd
        qr_code_url = user.qr_code.url if user.qr_code else None  # Obtener la URL del QR si existe
        try:
            # Usamos filter() en lugar de get() para obtener todas las transferencias
            history_user = Transference.objects.filter(idWallet = wallet_user.id)

            for history in history_user:
                history.type_transference == "reload"

            print(history_user)

            # Si no hay resultados, mostramos el mensaje
            #if not history_send.exists() or not history_request.exists():
                #message = "No tiene ni una transferencia"

        except Wallet.DoesNotExist:
            message = "No se encontró la billetera del usuario."

        return render(request, "transfer.html", {
                        'history_user': history_user,
                        'message': message,
                        'qr_code_url' : qr_code_url
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

            print("no")
            if Send.VerifyUser(usernameUser,request.user.username) and Send.VerifyAmount(request.user,send_money):
                
                print("si")
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
                    return redirect('transfer_widget')
                    
                except:
                    print("Error al realizar deposito")

        return render(request, "transfer.html", {"qr_code_url": qr_code_url})



# Create PDF

class Report():



    def generate_report_transference(request):
        wallet_user= Wallet.objects.get(user=request.user)
        history_user = Transference.objects.filter(idWallet = wallet_user.id)
        
        print(history_user)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="archivo.pdf"'

    # Configura el lienzo del PDF
        pdf = canvas.Canvas(response, pagesize=A4)
        width, height = A4  # Tamaño de página A4

        # Añade el título
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(width / 2 - 80, height - 100, "Historial de Transacciones")  # Centrado

        # Datos en formato vertical
        data = [
            ["Nombre", "Descripcion", "Monto","Tipo de transferencia","Fecha"],
            ["maria","nuevo pago","20.00","envio","2024-10-01"],
            # Agrega más filas según sea necesario
        ]
        for i in history_user:
            data.append([i.username,i.description,i.amount,i.type_transference,i.created_at])


        # Crea la tabla
        col_widths = [1.5 * inch] * len(data[0])  # 1.5 pulgadas para cada columna
        table = Table(data, colWidths=col_widths)

        # Estilo de la tabla
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Fondo gris para la primera fila
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Color de texto blanco para la primera fila
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alineación centrada
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente en negrita para el encabezado
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Espaciado para la primera fila
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Fondo beige para las demás filas
            ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Bordes de celda en negro
        ])
        table.setStyle(style)

        # Calcula la posición de la tabla en el centro
        x = (width - table.wrap(0, 0)[0]) / 2  # Centrado horizontalmente
        y = height - 150       # Debajo del título
            # Dibuja la tabla en el PDF
        table.wrapOn(pdf, width, height)
        table.drawOn(pdf, x, y)

        pdf.showPage()
        pdf.save()

        return response 




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