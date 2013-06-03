from .models import *
from django.contrib import admin

class ScopeAdmin(admin.ModelAdmin):
        list_display = ('scope', 'connector', 'description')
        class Meta:
                verbose_name = 'scope'


admin.site.register(Scope, ScopeAdmin)
