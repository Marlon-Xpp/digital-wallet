from django.urls import path

from user_auth import views

urlpatterns = [
    path("login/", views.login , name="login"),
    path("signup/", views.signup , name="signup"),
    path("verify/code/", views.verify_code, name="verify_code"),
    
    path("user/profile/", views.user_profile , name="user_profile"),
    path('verify/password/', views.verify_password, name='verify_password'),
    path('edit/profile/', views.edit_profile, name='edit_profile'),

    
]
