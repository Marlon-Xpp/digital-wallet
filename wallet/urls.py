from django.contrib import admin
from django.urls import path
from wallet import views

urlpatterns = [
#    path('', views.), #agregas las rutas desde el archivo views y la funcion que creaste

    path('wallet/manager_wallet.html',views.Account.PersonWallet,name="manager_wallet.html"),
    path('wallet/reload_money',views.Reload_money.get_recharge_view, name='reload_money')

]
