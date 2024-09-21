from django.contrib import admin
from .models import *  # Importa el modelo


admin.site.register(Wallet)

admin.site.register(User)

admin.site.register(Transference)
