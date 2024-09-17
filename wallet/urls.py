from django.contrib import admin
from django.urls import path
from wallet import views
urlpatterns = [
#    path('', views.), #agregas las rutas desde el archivo views y la funcion que creaste

path('',admin.site.urls),

]
