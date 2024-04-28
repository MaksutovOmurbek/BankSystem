from django.contrib import admin
from .models import User, HistoryTransfer
# Register your models here.
@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ['username', 'age', 'phone_number', 'wallet_address']
    
@admin.register(HistoryTransfer)
class AdminTransfer(admin.ModelAdmin):
    list_display = ['from_user', 'to_user', 'amount']