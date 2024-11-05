
from django.urls import path
from transactions import views
from transactions.models import Transference    

urlpatterns = [
    # path("send/receive", views.send_receive, name="send_receive"),
    path("transfer/qr", views.transfer_qr, name="transfer_qr"),
    path("transfer", views.Activity.transfer_widget, name="transfer_widget"),
    path("transfer/send", views.Send.transfer_send, name="transfer_send"),
    path("transfer/history", views.Activity.getHistory, name= "transfer_history"),
    
    path("transfer/pdf",views.Report.generate_report_transference, name="createPDF")
    # path("send/receive", views.send_receive, name="send_receive"),

]
