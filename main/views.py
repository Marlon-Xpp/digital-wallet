from django.shortcuts import render , redirect
from django.contrib.auth import logout


# Create your views here.
def index(request):
    return render(request, "index.html" , {"username": request.user.username})


def about(request):
    return render(request, "about.html", {"username": request.user.username})

def contact(request):
    return render(request, "contact.html", {"username": request.user.username})

def services(request):
    return render(request, "services.html", {"username": request.user.username})



    
    
def exit(request):
    logout(request)
    print("capturando la funcion")
    return redirect("index")


