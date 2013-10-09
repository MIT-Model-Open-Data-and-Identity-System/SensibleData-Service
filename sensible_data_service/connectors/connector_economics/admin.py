from .models import *
from django.contrib import admin


class ConnectorEconomicsAdmin(admin.ModelAdmin):
        list_display = ('name',)
        class Meta:
                verbose_name = 'connector'


admin.site.register(ConnectorEconomics, ConnectorEconomicsAdmin)
