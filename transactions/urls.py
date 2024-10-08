
from django.urls import path
from transactions import views
from transactions.models import Transference    

urlpatterns = [
    path("transfer/qr", views.transfer_qr, name="transfer_qr"),
    
     path("send/receive", views.Send.send_receive, name="send_receive"),
    # path("send/receive", views.send_receive, name="send_receive"),

    path('activity/',  views.Activity.getHistory, name="activity")

]
