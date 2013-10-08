from .models import ConnectorSbs2
from django.contrib import admin


class ConnectorSbs2Admin(admin.ModelAdmin):
	list_display = ('name',)
	class Meta:
		verbose_name = 'connector'


admin.site.register(ConnectorSbs2, ConnectorSbs2Admin)
