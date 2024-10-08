from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse

import stripe.webhook
from django.conf import settings

from wallet.models import Wallet 
from django.core.exceptions import ObjectDoesNotExist
from transactions.models import Transference

from share import models as ShareMD
import stripe

#Gestion del saldo
class Account():
    def __init__(self):
        self.user = ""
        
    @login_required 
    #Informacion sobre la Wallet
    def PersonWallet(request):
    # Obtener el usuario actual
        usuario_actual = request.user
        # Filtrar las wallets que pertenecen al usuario actual
        wallet_currency = Wallet.objects.filter(user=usuario_actual)
        return render(request,'wallet.html',{'wallet_currency' : wallet_currency })
        

    

class Reload_money():    

    def get_recharge_view(request):

        #api
        customer = stripe.Customer.create(
            name=user.get_full_name(),  # Usar el nombre completo del usuario
            email=user.email,           # Usar el email del usuario
            description="Cliente de la billetera"  # Descripción opcional 
            )

        producto = stripe.Product.create(
            name="Recarga de saldo",  # Nombre del producto
            description="Recarga de saldo en la billetera",  # Descripción del producto
            )

        payment = stripe.PaymentIntent.create(
            amount = request.POST.get("amount"),  # Monto en la moneda más pequeña, 5000 equivale a $50.00
            currency="PEN",  # Moneda en la que se realizará el pago
            customer=customer.id,  # Asocia este intento de pago con el cliente creado
            description="Recarga de saldo en la billetera",
            payment_method_types=["card"]  # Método de pago, puedes añadir más métodos
            )
        
        render(request,"reload_money.html",{})
    
    def get_api(self,amount):
        settings.STRIPE_TEST_API_KEY

        
        try:
            event = stripe.Webhook.construct_event()
        except:
            print("exit")
        return amount
        pass



@login_required(login_url='login')
def donation(request):
    stripe.api_key = settings.STRIPE_TEST_API_KEY
    
    user = request.user

    if request.method == 'POST':
        #daots del usuario lgueado
        name = request.POST.get('name')
        email = request.POST.get('email')
        amount = int(request.POST.get('amount'))  # Convertir a entero (centavos)
        payment_method_id = request.POST.get('payment_method_id')

        #creacion del customer
        customer = stripe.Customer.create(
            name=name,
            email=email
        )
        #creacion del producto
        product = stripe.Product.create(

        )

 # Crear un PaymentIntent para manejar el pago
            # Crear PaymentIntent sin confirmarlo
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='usd',
            payment_method_types=['card'],  # Puedes agregar otros métodos de pago aquí
        )


        # Devolver la respuesta como JSON
        return JsonResponse({
            'success': True,
            'message': 'Gracias por tu donación!',
            'payment_intent': payment_intent.id
        })
    
    # Si es GET, renderiza el formulario de donación
    return render(request, 'donativo.html')

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
@login_required
def activity(request):
    return render(request, "activity.html", {"username": request.user.username})