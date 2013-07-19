from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from accounts.models import Participant, UserRole

class ParticipantInline(admin.StackedInline):
	model = Participant
	can_delete = True
	verbose_name_plural = 'participant'

class UserRoleInline(admin.StackedInline):
	model = UserRole
	can_delete = True

class UserAdmin(UserAdmin):
	inlines = (ParticipantInline, UserRoleInline)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
