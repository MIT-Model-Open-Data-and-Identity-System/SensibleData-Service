from .models import *
from django.contrib import admin


class ConnectorFunfAdmin(admin.ModelAdmin):
        list_display = ('name',)
        class Meta:
                verbose_name = 'connector'


admin.site.register(ConnectorFunf, ConnectorFunfAdmin)
