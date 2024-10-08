# Importaciones estándar
import random
import re
import requests
import json
from django.utils.crypto import get_random_string
# Importaciones de terceros
from email_validator import validate_email as email_validator, EmailNotValidError


# Importaciones de Django
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone


# Importaciones de tu aplicación
from user_auth.models import CustomUser
from .models import LoginAttempt


import qrcode
import io
from django.core.files import File


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
    """Verifica que el correo electrónico tenga un formato válido y exista."""
    try:
        # Validar el correo electrónico y obtener un diccionario con el formato validado
        valid = email_validator(email)
        # Si necesitas acceder a la dirección válida:
        return valid['email']  # Esto te da el correo validado y corregido
    except EmailNotValidError as e:
        # La dirección de correo no es válida
        raise ValidationError(f"El correo electrónico no tiene un formato válido: {str(e)}")

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
    print("Entrando a la función verify_code")
    print("Método recibido:", request.method)
    if request.method == 'POST':
        # Obtener los datos de la solicitud JSON
        try:
            data = json.loads(request.body)
            input_code = data.get('verification_code')
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Error en el formato de los datos enviados.'})

        session_code = request.session.get('verification_code')
        email = request.session.get('email')
        
        # Verificar si el código de sesión existe
        if session_code is None:
            return JsonResponse({'success': False, 'error': 'No se encontró el código de verificación en la sesión.'})

        try:
            if str(input_code) == str(session_code):
                # Activar la cuenta del usuario
                user = CustomUser.objects.get(email=email)
                user.is_active = True
                user.save()

                # Limpiar la sesión después de la verificación
                del request.session['verification_code']
                del request.session['email']

                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'El código de verificación es incorrecto.'})

        except CustomUser.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Usuario no encontrado.'})

        except Exception as e:
            return JsonResponse({'success': False, 'error': 'Ocurrió un error inesperado. Por favor, inténtelo de nuevo.'})
    
    print("Método recibido:", request.method)
    return JsonResponse({'success': False, 'error': 'Método no permitido.'})



def lookup_phone_number(phone_number, country_code):
    api_key = settings.NUMLOOKUP_API_KEY  # Acceder a la clave desde settings
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
        return {'error': 'error behind the method', 'details': str(e), 'number': phone_number, 'api': api_key}


def validate_phone_number(phone_number, country_code):
    api_key = settings.NUMLOOKUP_API_KEY  # Acceder a la clave desde settings
    url = f"https://api.numlookupapi.com/v1/validate/{country_code}{phone_number}?apikey={api_key}"
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            valid = data.get('valid')
            if not valid:
                raise ValidationError("El número no existe, intenta con otro")
        else:
            return {'error': f"Error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {'error': 'error behind the method', 'details': str(e), 'number': phone_number, 'api': api_key}


def phone_lookup_view(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        country_code = request.POST.get('country_code')
        try:
            # Consultar el API usando la función que ahora accede al API Key directamente
            result = lookup_phone_number(phone_number, country_code)
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({'error': 'number null', 'details': str(e), 'number': phone_number, 'country_code': country_code}, status=500)
    return render(request, 'prueba.html')



def generate_emvco_qr_code(user, amount=None, currency="604", country="PE", city="Lima"):
    # Crear datos estructurados según el estándar EMVCo QR
    emvco_data = [
        "00", "01",  # Payload format indicator
        "01", "12",  # Point of Initiation Method (QR dinámico)
        "39", f"user_{user.username}",  # Username del usuario
        "52", "0000",  # Merchant Category Code (0000 es genérico)
        "53", currency,  # Código de la moneda (ISO 4217: 604 para Soles)
        "58", country,  # Código del país (PE para Perú)
        "59", "WopyPay",  # Nombre de la plataforma
        "60", city,  # Ciudad del comercio o usuario
        # Monto se puede agregar después
        # AQUI FALTA AGREGAR EL CHECKSUM (lo agregaremos al final)
    ]

    # Si se proporciona un monto, añadirlo
    if amount is not None:
        emvco_data.append("54")
        emvco_data.append(f"{amount:.2f}")  # Monto a transferir

    # Unir los datos en el formato correcto EMVCo (ejemplo: tag+length+value)
    qr_data = "".join([f"{tag}{len(value):02}{value}" for tag, value in zip(emvco_data[::2], emvco_data[1::2])])

    # Calcular CRC y añadir al final
    crc = calculate_crc(qr_data)
    qr_data += crc  # Añadir el CRC al final de los datos

    # Generar el código QR
    qr = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2,
    )
    
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")

    # Guardar la imagen en el campo qr_code del usuario
    user.qr_code.save(f"user_{user.username}_qr.png", File(buffer), save=False)
    user.save()

def calculate_crc(data):
    # Usamos el algoritmo CRC-CCITT (XModem) para el cálculo
    crc = 0xFFFF
    polynomial = 0x1021

    for byte in bytearray(data, 'utf-8'):
        crc ^= (byte << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ polynomial
            else:
                crc <<= 1
            crc &= 0xFFFF  # Asegurarnos de que el CRC sigue siendo de 16 bits

    return format(crc, '04X')


#funcion para registrar a los usuarios
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
            
            validate_phone_number(phone_number,country_code)
            
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
            
            # # Generar y guardar la clave de encriptación
            # user.encryption_key = get_random_string(32).encode()  # Generar una clave aleatoria
            # user.save()
            
            # #generamos el código QR para el usuario
            generate_emvco_qr_code(user)
            
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
            return render(request, "signup.html", {
                'verification_sent': True, #le pasamos true para q pueda seguir con su flujo
                'email': email  #le pasamos el email capturado
            })
        
        
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


#funcion para logear al usuario
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        try:
            validate_fields(username=username, password=password)
            
            ip_address = request.META.get('REMOTE_ADDR')
            attempts = LoginAttempt.objects.filter(username=username, ip_address=ip_address)
            
            # Verificar si se han superado los intentos permitidos
            if attempts.count() >= settings.MAX_ATTEMPTS:
                last_attempt = attempts.order_by('-timestamp').first()
                if last_attempt and last_attempt.timestamp + settings.BLOCK_TIME > timezone.now():
                    print("Demasiados intentos. Por favor, inténtalo más tarde.")
                    return render(request, "login.html", {"error": "Demasiados intentos. Por favor, inténtalo más tarde."})

            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                attempts.delete()# Eliminar registros de intentos fallidos
                #inciar sesion a nivel de backend para avisarles a las funciones que el usaurio esta logeado
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




#Funcion para mostrar los datos del usuario

@login_required
def user_profile(request):
    user = request.user  

    # if request.method == 'POST':
    #     new_email = request.POST.get('email')

    #     # Validar el nuevo correo
    #     try:
    #         validated_email = validate_email(new_email)
    #     except ValidationError as e:
    #         messages.error(request, str(e))
    #         return JsonResponse({'success': False, 'message': str(e)}, status=400)  # Devuelve error

    #     verification_code = generate_verification_code()

    #     try:
    #         send_mail(
    #             'Código de verificación',
    #             f'Tu código de verificación es: {verification_code}',
    #             settings.DEFAULT_FROM_EMAIL,
    #             [validated_email],
    #             fail_silently=False,
    #         )
    #         request.session['verification_code'] = verification_code
    #         request.session['new_email'] = validated_email
            
    #         messages.success(request, 'Se ha enviado un código de verificación a tu nuevo correo. Por favor, verifica tu correo.')
    #         return JsonResponse({'success': True, 'redirect': 'verify/code'})  # Devuelve la redirección
    #     except Exception as e:
    #         messages.error(request, f'Error al enviar el correo: {str(e)}')
    #         return JsonResponse({'success': False, 'message': str(e)}, status=400)  # Devuelve error
    
    return render(request, "user_profile.html", {"user": user})




@login_required
def verify_password(request):
    if request.method == "POST":
        password = request.POST.get('password')
        user = authenticate(username=request.user.username, password=password)

        if user is not None:
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})

    return JsonResponse({'success': False})


#FALTA IMPLEMENTAR LOGICA PARA LA VERIFICACION DE UN 
#CORREO VALIDO Y NO REISTREN UN CORREO Q NO SEA VALIDO O Q NO EXISTA
@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')
        user.save()  # Guardamos los cambios

        return redirect('user_profile')  # Redirigimos al perfil una vez actualizado

    return redirect('user_profile')