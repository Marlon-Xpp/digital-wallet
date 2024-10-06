from django.contrib import admin
from .models import *  # Importa el modelo

from user_auth import models


admin.site.register(Wallet)

admin.site.register(models.CustomUser)


