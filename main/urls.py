from django.urls import path
from main import views

urlpatterns = [
    path("", views.Index, name="index"),
    path("about", views.About, name="about"),
    path("contact", views.Contact, name="contact"),
]
