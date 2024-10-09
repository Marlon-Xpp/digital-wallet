from django.contrib import admin
from django.urls import path
from wallet import views

urlpatterns = [
    

    path('wallet/operations',views.Account.operations,name="operations"),
    path('wallet/manager_money',views.Account.PersonWallet,name="manager_money"),
    path('wallet/reload_money',views.Reload_money.get_recharge_view, name='reload_money'),

    path('wallet/reload_money/success_payment',views.Reload_money.payment_success, name='success_payment'),
    path('wallet/reload_money/failure_payment',views.Reload_money.payment_failure, name='failure_payment')

]
