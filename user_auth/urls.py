from django.urls import path

from user_auth import views

urlpatterns = [
    path("login/", views.Login , name="login"),
    path("signup/", views.Signup , name="signup"),
    
]
