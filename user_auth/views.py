from django.shortcuts import render, redirect
from django.contrib import messages
from user_auth.models import CustomUser
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
import re

from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
import random
from .models import LoginAttempt
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse


from .models import LoginAttempt
from django.utils import timezone
from datetime import timedelta

import requests

#clases importadas

# Create your views here.
#AQUI VA LA LOGICA  DE LA APLICACION AUTH USER

#FUNCIONALIDADES DEL AUTH_USER
#Registro de usuarios:
#Inicio de sesión y cierre de sesión:
#Bloquear intentos fallidos (nivel de seguridad)
#Restablecimiento de contraseña(opcional)
#Edición de perfil:
#Cambio de contraseña(opcional)
#Seguridad del perfil:




def validate_email(email):
    """Verifica que el correo electrónico tenga un formato válido."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValidationError("El correo electrónico no tiene un formato válido.")

def validate_password(password):
    """Verifica que la contraseña cumpla con ciertos criterios de complejidad."""
    if len(password) < 8:
        raise ValidationError("La contraseña debe tener al menos 8 caracteres.")
    if not re.search(r'\d', password):
        raise ValidationError("La contraseña debe contener al menos un número.")
    if not re.search(r'[A-Z]', password):
        raise ValidationError("La contraseña debe contener al menos una letra mayúscula.")
    if not re.search(r'[a-z]', password):
        raise ValidationError("La contraseña debe contener al menos una letra minúscula.")
    if not re.search(r'[@$!%*?&]', password):
        raise ValidationError("La contraseña debe contener al menos un carácter especial.")
    
    
# cradno una funcion ade validacion para los campos vacios y con n argumentos
def validate_fields(**fields):
    #aplicamos un for para recorrer la tupla y guardr los datos de fields a field 
    for field_name, field_value in fields.items():
        #aqui verificamos uno x uno el campo field si esta vacio y si fiel no hay nd 
        if not field_value:
            #si tan solo un campo esta vacio se mostrar el mensaje de error
            print(f"El campo {field_name} no puede estar vacío")
            #se detentra el codigo y mostrar el error con el msj 
            raise ValidationError(f"El campo {field_name} no puede estar vacio")

#funcion para generar codigo de verificacion del usuario
def generate_verification_code():
    return random.randint(10000, 99999)

#funcion para notificar al usaurio 
# def notification_user(request):
#     print pass


#verificar si existen los datos en la base de datos
def verify_exists(**fields):
    # Iterar sobre los campos proporcionados
    for field_name, field_value in fields.items():
        # Filtrar usando el campo actual
        if CustomUser.objects.filter(**{field_name: field_value}).exists():
            # Lanza una excepción inmediatamente con un mensaje específico
            raise ValidationError(f"El {field_name} ya existe, intenta con otro.")




# Funcion para verificar el codigo y la activacion de su cuenta
def verify_code(request):
    if request.method == 'POST':
        input_code = request.POST.get('verification_code')
        session_code = request.session.get('verification_code')
        email = request.session.get('email')
        
        
        # Verificar si el código de sesión existe
        if session_code is None:
            messages.error(request, "No se encontró el código de verificación en la sesión.")
            return render(request, "verify_code.html")

        try:
            
            if str(input_code) == str(session_code):
                # Activar la cuenta del usuario
                user = CustomUser.objects.get(email=email)
                user.is_active = True
                user.save()

                # Limpiar la sesión después de la verificación
                del request.session['verification_code']
                del request.session['email']
                
                print("se elimino los datos de la sesion anterior, y tu cuenta se activo")
                messages.success(request, '¡Tu cuenta ha sido activada!')
                return redirect('login')

            else:
                print("el codigo de verificacion es incorecto")
                messages.error(request, 'El codigo de verificacion es incorrecto')
                raise ValidationError('El código de verificación es incorrecto.')
                
                
        except ValidationError as e:
            messages.error(request, str(e))
            return render(request, "verify_code.html", {"error": str(e)})
        
        except Exception as e:
            print(f"el error global es: {e}")
            return render(request, "verify_code.html", {"error": "el error inesperado dentro del codigo"} )
            
    return render(request, 'verify_code.html')



APIKEYCOUNTRY = 'num_live_EUGXAxGMNzGUyImA1Ck1OP6d9vEVzohR5vj3taIp'  # Número máximo de intentos permitidos

def validate_phone_number(phone_number,country_code,api_key):
    url = f"https://api.numlookupapi.com/v1/validate/{country_code}{phone_number}?apikey={api_key}"
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200: 
            data  = response.json()
            valid = data.get('valid')
            if valid != True :
                raise ValidationError("el numero no existe, intenta con otro")
        else:
            return {'error': f"Error: {response.status_code} - {response.text}"}
    except Exception as e:
        return JsonResponse({'error': 'error behind the method', 'details': str(e),'number': phone_number,'api': api_key}, status=500)


def signup(request):
    if request.method == "POST":
        #Obtener los datos de entrada y limpiamos los espacios en blaco del incio y del final del texto
        #Evitar errores pasamos un campo vacio como por defecto
        names = request.POST.get("names","").strip()
        lastname = request.POST.get("lastname","").strip()
        username = request.POST.get("username","").strip()
        phone_number = request.POST.get("phone_number","").strip() #modificas si es necesario
        country_code = request.POST.get("country_code","").strip()
        email = request.POST.get("email","").strip()
        password = request.POST.get("password","").strip()
        
        # manejar alguna error que puede suceder dentro del codigo
        try:
            #validar que los campos ingresado por el usaurio no esten vacios
            validate_fields(names=names, lastname=lastname, username=username, email=email, password=password, phone=phone_number, country_code=country_code)
            #verificacion del formato del correo
            validate_email(email)
            #validacion de la contraseña
            validate_password(password)
            #validacion para corrobar si ya existen
            verify_exists(username=username, email=email)
            if CustomUser.objects.filter(phone = phone_number).exists():
                print("el numero telefonico ya esta registrado")
                raise ValidationError("ingresa otro numero telefonico")
            
            validate_phone_number(phone_number,country_code,APIKEYCOUNTRY)
            
            user = CustomUser(
                first_name = names,
                last_name = lastname,
                username = username,
                email = email,
                phone= phone_number,
                country_code = country_code,
                password = make_password(password), # es mucho mas seguro q usar hash siempre y mas recomndable usar make_password para hacear contraseñas a nivel de seguridad
                is_active = False,
            )
            #aqui se guardara los datos obtenidos ala base de datos
            user.save()
            #imprimimos un msj de exito
            print("Usuario guardado correctamente. pero esta inactivo")
            
            #generamos el codigo de verificacion
            verification_code = generate_verification_code()
            
            #Guardar el código en la sesión para la verificación posterior
            request.session["verification_code"] = verification_code 
            request.session["email"] = email
            
            #Enviamos el correo con el codigo de verificacion
            # Enviamos el correo con el código de verificación
            send_mail(
                "Código de verificación", #asunto
                f"Tu código de verificación es: {verification_code}", # mensaje
                settings.DEFAULT_FROM_EMAIL, #remitente
                [email],  # email del destinatario
                fail_silently=False, #detectar alguna error
            )
            
            print("Se ha enviado un codigo de verificacion a tu correo")
            messages.success(request, "Se ha enviado un codigo de verificacion a tu correo")
            
            #retornamos y redirigimos a la vista de login
            return redirect("verify_code")
        
        
        #capturamos los errores que creamos para q se muestren x aqui
        except ValidationError as e:
            print(f"La autenticación falló: {e}")
            messages.error(request, str(e))
            return render(request, "signup.html", {'error': str(e)} )
        #capturamos un erro general dentro del codigo
        except Exception as e:
            #retornamos y imprimimos el msj de error general dentro del codigo
            print(f"el error es el siguiente global dentro del codigo: {e}")
            
            return render(request, "signup.html", {"error": "eror inesperado. profavor intente de nuevo"})
    #retornamos la vista princiapl del signup y lo msotramos 
    return render(request, "signup.html")





MAX_ATTEMPTS = 5  # Número máximo de intentos permitidos
BLOCK_TIME = timedelta(seconds=15)  # Tiempo de bloqueo de 15 segundos se cambiara el tiempo

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        try:
            validate_fields(username=username, password=password)
            
            ip_address = request.META.get('REMOTE_ADDR')
            attempts = LoginAttempt.objects.filter(username=username, ip_address=ip_address)
            
            # Verificar si se han superado los intentos permitidos
            if attempts.count() >= MAX_ATTEMPTS:
                last_attempt = attempts.order_by('-timestamp').first()
                if last_attempt and last_attempt.timestamp + BLOCK_TIME > timezone.now():
                    print("Demasiados intentos. Por favor, inténtalo más tarde.")
                    return render(request, "login.html", {"error": "Demasiados intentos. Por favor, inténtalo más tarde."})

            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                attempts.delete()# Eliminar registros de intentos fallidos
                auth_login(request, user)
                print("la autentificacion fue exitosa")
                return redirect("index")  # Redirigir a la vista deseada
            else:
                # Registrar el intento fallido
                LoginAttempt.objects.create(username=username, ip_address=ip_address)
                print("La autenticación fue fallida.")
                return render(request, "login.html", {"error": "La autenticación fue fallida."})
            
        except ValidationError as e:
            print(f"el error es : {e}")
            return render(request, "login.html", {"error": str(e)})
        except Exception as e:
            print(f"el error de exception es : {e}")
            return render(request, "login.html", {"error": "Ocurrió un error inesperado."})
    
    # Si es un GET, solo muestra el formulario
    return render(request, "login.html")


#para las funciones snake_case
#para las clases CamelCase o PascalCase



@login_required
def user_profile(request):
    
    return render(request, "user_profile.html", {"username": request.user.username})



# Función que consulta el API
def lookup_phone_number(api_key, phone_number,country_code):
    url = f"https://api.numlookupapi.com/v1/validate/{country_code}{phone_number}?apikey={api_key}"
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200: 
            return response.json()
        else:
            return {'error': f"Error: {response.status_code} - {response.text}"}
    except Exception as e:
        return JsonResponse({'error': 'error behind the method', 'details': str(e),'number': phone_number,'api': api_key}, status=500)
    
# Vista para recibir el número y mostrar el resultado
def phone_lookup_view(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        country_code = request.POST.get('country_code')
        api_key = APIKEYCOUNTRY  # Sustituir con tu API Key
        print(type(phone_number))
        try:
            # Consultar el API
            result = lookup_phone_number(api_key, phone_number,country_code)
            # Devolver los resultados en formato JSON
            return JsonResponse(result)
        except Exception as e:
            # Captura cualquier otro tipo de excepción
            return JsonResponse({'error': 'number null', 'details': str(e),'number': phone_number, 'country_code':country_code}, status=500)
    # En caso de GET, muestra la página con el formulario
    return render(request, 'prueba.html')
