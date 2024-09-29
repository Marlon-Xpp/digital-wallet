
from django.urls import path
from transactions import views

urlpatterns = [
    path("send/receive", views.send_receive, name="send_receive"),
    
    # path("send/receive", views.send_receive, name="send_receive"),
    # path("send/receive", views.send_receive, name="send_receive"),
    
]
