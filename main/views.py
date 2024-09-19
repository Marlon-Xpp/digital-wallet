from django.shortcuts import render , redirect
from django.contrib.auth import logout


# Create your views here.
def index(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

def services(request):
    return render(request, "services.html")

def exit(request):
    logout(request)
    print("capturando la funcion")
    return redirect("index")


