from django.contrib import admin
from django.urls import path
from .views import Account,Transference , Send
from wallet import views
urlpatterns = [
#    path('', views.), #agregas las rutas desde el archivo views y la funcion que creaste

#from .views import 
    #path('profile/', UserProfile.as_view(), name='profile'),
   # path('profile/edit/', UserProfileUpdate.as_view(), name='profile_update'),



     path('wallet/PersonWallet',Account.PersonWallet,name="wallet_PersonWallet"),
    
     path('wallet/sendUser',Send.sendUser, name="send_User"),
    
     #path('wallet/get',)

   # path('receive/',OptionsMoney.ReceiveMoneyFrom, name="receive"),


    #path('activity/', ActivityList.as_view(), name='activity'),
    #path('send/', SendSear chUser.as_view(), name='send'),
    #path('send/<int:pk>/', SendMoney.as_view(), name='send_money'),
    #path('send/success/', SendSuccess.as_view(), name='send_success'),
    #path('request/', RequestSearchUser.as_view(), name='request'),
    #path('request/<int:pk>/', RequestMoney.as_view(), name='request_money'),
    #path('request/success/', RequestSuccess.as_view(), name='request_success'),



    #path('history/',Transference.HistoryTransferSend, name="history"),

    path('activity/',  views.Activity.getHistory, name="activity")
]
