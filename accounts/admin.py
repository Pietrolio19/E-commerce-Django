from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('Informazioni aggiuntive', {
            'fields': ('name', 'surname', 'address', 'city', 'state', 'CAP', 'is_store_manager')
        }),
    )