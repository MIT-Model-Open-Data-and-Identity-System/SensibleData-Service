from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from accounts.models import Participant

class ParticipantInline(admin.StackedInline):
	model = Participant
	can_delete = True
	verbose_name_plural = 'participant'

class UserAdmin(UserAdmin):
	inlines = (ParticipantInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
