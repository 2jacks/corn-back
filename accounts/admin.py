from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

from geo.models import Farmer


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class FarmerInline(admin.StackedInline):
    model = Farmer
    can_delete = False
    verbose_name_plural = 'farmer'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (FarmerInline,)


# Re-register UserAdmin
admin.site.register(User, UserAdmin)

