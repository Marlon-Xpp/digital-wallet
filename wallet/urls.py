from django.contrib import admin
from django.urls import path
from wallet import views

urlpatterns = [
    

    path('operations/',views.Account.operations, name="operations"),
    path('manager/money/',views.Account.PersonWallet, name="manager_money"),
    path('reload/money/',views.Reload_money.get_recharge_view, name='reload_money'),

    path('reload/money/success_payment/',views.Reload_money.payment_success, name='success_payment'),
    path('reload/money/failure_payment/',views.Reload_money.payment_failure, name='failure_payment')

]
