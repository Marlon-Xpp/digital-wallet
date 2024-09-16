from django.urls import path

from user_auth import views

urlpatterns = [
    path("", views.Home , name="home"), #agregas las rutas desde el archivo views y la funcion que creaste
    path("login/", views.Login , name="login"),
    path("signup/", views.Signup , name="signup"),
    
]
