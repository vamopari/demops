# Register your models here.
from django.contrib import admin
from rest_framework_api_key.admin import APIKeyModelAdmin
from .models import ClientAPIKey, Client, Tenant


@admin.register(ClientAPIKey)
class ClientAPIKeyModelAdmin(APIKeyModelAdmin):
    pass


@admin.register(Client)
class ClientModelAdmin(admin.ModelAdmin):
    pass

@admin.register(Tenant)
class TenantModelAdmin(admin.ModelAdmin):
    pass