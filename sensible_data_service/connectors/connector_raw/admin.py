from .models import *
from django.contrib import admin


class ConnectorRawAdmin(admin.ModelAdmin):
	list_display = ('name',)
	class Meta:
		verbose_name = 'connector'


admin.site.register(ConnectorRaw, ConnectorRawAdmin)
