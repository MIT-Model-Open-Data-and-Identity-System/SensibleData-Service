from .models import *
from django.contrib import admin


class ConnectorEconomicsAdmin(admin.ModelAdmin):
    list_display = ('name',)
    class Meta:
        verbose_name = 'connector'

admin.site.register(ConnectorEconomics, ConnectorEconomicsAdmin)

class VouchersAdmin(admin.ModelAdmin):
    list_display = ('voucher', 'won_by', 'won_at')

admin.site.register(Voucher, VouchersAdmin)