from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse

import stripe.webhook
from django.conf import settings

from wallet.models import Wallet 
from django.core.exceptions import ObjectDoesNotExist
from transactions.models import Transference

from share import models as ShareMD
import stripe



#FUNCIONALIDADES
#Gestión del saldo:
#Envío de dinero:
#Recepción de dinero:
#Historial de transacciones:
#Seguridad de las transacciones:
#Integraciones con servicios de pago externos (opcional):

#conversion de moneda
#asociar terjeta real a nuestra wallet
#retiro de dinerp

#factura electronica
#descaragr la infromacion del historial de trasacciones en pdf
#comprar en linea con billetera digital




#Gestion del saldo
class Account():
    def __init__(self):
        self.user = ""
        
    def first_wallet(user):
        #wallet.save()
        wallet = Wallet(user = user)
        wallet.save()
        return True

    @login_required(login_url='login')
    #Informacion sobre la Wallet
    def PersonWallet(request):
        
        # Obtener el usuario actual
        wallet_currency = Wallet.objects.get(user=usuario_actual)
        usuario_actual = request.user
        
        # Filtrar las wallets que pertenecen al usuario actual
        return render(request,'manager_money.html',{
            'wallet_balance': wallet_currency.get_balance(),
            
        })


    def operations(request):
        wallet_currency = Wallet.objects.get(user= request.user)
        user = request.user  # Obtener el usuario autenticado de la bd
        qr_code_url = user.qr_code.url if user.qr_code else None  # Obtener la URL del QR si existe
        return render(request,'operations.html', {
            'wallet_balance' : wallet_currency.get_balance(),
            'stripe_public_key' : settings.STRIPE_TEST_API_KEY,
            #traer la imagen
            'qr_code_url': qr_code_url,
        })    

class Reload_money():    
    @login_required(login_url='login')
    def get_recharge_view(request):
        stripe.api_key = settings.STRIPE_TEST_API_KEY
        user = request.user
        amount = request.POST.get("amount")

        print("ejecutando - 1")
        if request.method == "POST":

            print("ejecutando - 2")

            product = stripe.Product.create(
                name=f"Recarga movil de {amount} al usuario { user.username}"
            )

            price_data = stripe.Price.create(
                currency= "PEN",
                product= product.id,
                unit_amount= transform.transform_amount(amount,True)

            )


            check_sesion = stripe.checkout.Session.create(
                payment_method_types=['card'],  # Solo habilitar pagos con tarjeta
    
                line_items=[
                    {
                        'price': price_data.id,
                        'quantity': 1,
                    }
                ],

                mode='payment',
                success_url= request.build_absolute_uri(reverse('success_payment')),
                cancel_url= request.build_absolute_uri(reverse('failure_payment')),
            )

            request.session['amount'] = float(amount)  # Store the amount as a float in the session


            return redirect(check_sesion.url)

        return render(request,"reload_money.html",{})
    
    @login_required(login_url='login')
    def payment_success(request):
        
        user = request.user
        amount_reload = request.session.get('amount',None)
        
        wallet_reload = Wallet.objects.get(user = user)

        wallet_reload.add_funds(amount_reload)

        #Eliminar monto de session
        del request.session['amount']

        return render(request, 'verify_payment/success.html')

    def payment_failure(request):
        return render(request, 'verify_payment/failure.html')


class transform():
    def transform_amount(amount, to_cents=True):

        if to_cents:
            # Convert from decimal to cents
            return int(float(amount) * 100)
        else:
            # Convert from cents to decimal
            return float(amount) / 100


class recieve_money():
    payout = stripe.Payout.create














def product_page(request):
    
    if request.method == 'POST':
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': 2.00,
                    'quantity': 1,
                }
            ],
            mode='payment',
            customer_creation= 'always',
            success_url='/paymente_successful?session_id={}',
            cancel_url='/payment_cancelled',
        
        ),
        return redirect(checkout_session.url, code =303)
    return JsonResponse()

def a():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'precio_id',  # Reemplaza con el ID del precio creado
            'quantity': 1,
        }],
        mode='payment',
        success_url='https://tu_sitio.com/exito?session_id={CHECKOUT_SESSION_ID}',
        cancel_url='https://tu_sitio.com/cancelar',
    )
    return redirect(session.url, code=303)

#Historial de transacciones:
class Activity(Account):
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

        except Wallet.DoesNotExist:
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
        
        
        
#Integraciones con servicios de pago externos (opcional) Api:


class ValidationError():
    def __init__(self) -> None:
        pass

    

#FUNCIONALIDADES
#Gestión del saldo:
#Envío de dinero:
#Recepción de dinero:
#Historial de transacciones:
#Seguridad de las transacciones:
#Integraciones con servicios de pago externos (opcional):



#conversion de moneda
#asociar tarjeta
#factura.

#descargar en un pdf el historial

#subir a la nube 

@login_required
def activity(request):
    return render(request, "activity.html", {"username": request.user.username})