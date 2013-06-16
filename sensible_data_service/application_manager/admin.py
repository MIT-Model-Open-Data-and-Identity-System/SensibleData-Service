from oauth2app.models import *
from django.contrib import admin
from .models import *

class ApplicationAdmin(admin.ModelAdmin):
        list_display = ('name', 'user', 'client')

admin.site.register(Application, ApplicationAdmin)

class ParameterAdmin(admin.ModelAdmin):
        list_display = ('key', 'value')

admin.site.register(Parameter, ParameterAdmin)
