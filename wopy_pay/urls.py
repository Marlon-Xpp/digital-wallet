"""
URL configuration for wopy_pay project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls")),
    path("auth/", include("user_auth.urls"), name="auth"),
    path("account/", include("wallet.urls"), name="wallet"), 
    path("transactions/", include("transactions.urls"), name="transactions"), 
    
    

    #path("wallet/", include("wallet.urls"), name="wallet"), #aqui incluimos todas las urls del archivo wallet
    #path("auth/", include("auth.urls"), name="auth"), #aqui incluimos todas las urls del archivo auth
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
