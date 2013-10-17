from .models import *
from django.contrib import admin


class ConnectorAnswerAdmin(admin.ModelAdmin):
	list_display = ('name',)
	class Meta:
		verbose_name = 'connector'

admin.site.register(ConnectorAnswer, ConnectorAnswerAdmin)

class ConnectorAnswerEndpointAdmin(admin.ModelAdmin):
	list_display = ('question','answer', 'active')

admin.site.register(ConnectorAnswerEndpoint, ConnectorAnswerEndpointAdmin)
