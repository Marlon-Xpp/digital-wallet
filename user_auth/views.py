from django.shortcuts import render

# Create your views here.
#AQUI VA LA LOGICA  DE LA APLICACION AUTH USER


def Home(reques):
    return render(reques, 'home.html')

def Signup(request):
    return render(request, "signup.html")

def Login(request):
    return render(request, "login.html")