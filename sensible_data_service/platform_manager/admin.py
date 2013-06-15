from .models import *
from django.contrib import admin

class PlatformScopeAdmin(admin.ModelAdmin):
        list_display = ('key', 'description')
        class Meta:
                verbose_name = 'scope'

class PlatformCodeAdmin(admin.ModelAdmin):
        list_display = ('user', 'code', 'exchanged', 'time_generated', 'time_exchanged')
        class Meta:
                verbose_name = 'authorization code'

class PlatformAccessTokenAdmin(admin.ModelAdmin):
        list_display = ('user', 'token', 'token_type', 'refresh_token', 'expire')
        class Meta:
                verbose_name = 'acess token'


admin.site.register(PlatformScope, PlatformScopeAdmin)
admin.site.register(PlatformCode, PlatformCodeAdmin)
admin.site.register(PlatformAccessToken, PlatformAccessTokenAdmin)
