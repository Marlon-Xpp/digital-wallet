from django.urls import path

from user_auth import views

urlpatterns = [
    path("login/", views.login , name="login"),
    path("signup/", views.signup , name="signup"),
    path("user/profile/", views.user_profile , name="user_profile"),
    path("verify/code", views.verify_code, name="verify_code")
    
    
]
