from .models import *
from django.contrib import admin

class ScopeAdmin(admin.ModelAdmin):
        list_display = ('key', 'description')
        class Meta:
                verbose_name = 'scope'

class CodeAdmin(admin.ModelAdmin):
        list_display = ('user', 'code', 'exchanged', 'time_generated', 'time_exchanged')
        class Meta:
                verbose_name = 'authorization code'

class AccessTokenAdmin(admin.ModelAdmin):
        list_display = ('user', 'token', 'token_type', 'refresh_token', 'expire')
        class Meta:
                verbose_name = 'acess token'


admin.site.register(Scope, ScopeAdmin)
admin.site.register(Code, CodeAdmin)
admin.site.register(AccessToken, AccessTokenAdmin)
