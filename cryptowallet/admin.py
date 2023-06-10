from django.contrib import admin
from .models import KRWBalance, CryptoBalance

# Register your models here.

admin.site.register(KRWBalance)
admin.site.register(CryptoBalance)
