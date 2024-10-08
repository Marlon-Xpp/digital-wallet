
from django.urls import path
from transactions import views

urlpatterns = [
    path("send/receive", views.send_receive, name="send_receive"),
    path("transfer/qr", views.transfer_qr, name="transfer_qr"),
    
    # path("send/receive", views.send_receive, name="send_receive"),
    # path("send/receive", views.send_receive, name="send_receive"),
    
]
