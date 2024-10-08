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



# Create your views here.

#AQUI VA LA LOGICA  DE LA APLICACION WALLET

#Gestion del saldo
class Account():
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
        
    @login_required 
    #Informacion sobre la Wallet
    def PersonWallet(request):
    # Obtener el usuario actual
        usuario_actual = request.user
    
        # Filtrar las wallets que pertenecen al usuario actual
        wallet_currency = Wallet.objects.filter(user=usuario_actual)
        

        return render(request,'wallet.html',{'wallet_currency' : wallet_currency })


#Envío de dinero:

    

class paymethod():
    def __init__(self) -> None:
        pass

    def get_api():
        #Utilizancion del api de metodo pago, para obtener el pago directo a la app
        pass

    def get_method():
        pass


class Recharge():    
    def get_recharge_view(request):
        #api

        render(request,"",{})

    def get_api(self,amount):


        customer = stripe.Customer.create()
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