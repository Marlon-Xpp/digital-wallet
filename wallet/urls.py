from django.urls import path
from wallet import views
urlpatterns = [
#    path('', views.), #agregas las rutas desde el archivo views y la funcion que creaste
     path('activity/', views.activity, name="activity")
]
