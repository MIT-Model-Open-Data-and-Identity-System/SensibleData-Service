from .models import *
from django.contrib import admin

class AuthorizationAdmin(admin.ModelAdmin):
	list_display = ('user', 'application', 'scope', 'active', 'created_at', 'revoked_at')

admin.site.register(Authorization, AuthorizationAdmin)

class GcmRegistrationAdmin(admin.ModelAdmin):
	list_display = ('user', 'device_id', 'gcm_id')

admin.site.register(GcmRegistration, GcmRegistrationAdmin)
