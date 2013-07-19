from oauth2app.models import *
from django.contrib import admin
from .models import *

class TosAcceptanceAdmin(admin.ModelAdmin):
        list_display = ('user', 'version', 'lang', 'accepted_at')

admin.site.register(TosAcceptance, TosAcceptanceAdmin)
