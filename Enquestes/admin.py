from django.contrib import admin
from django.contrib.admin import ModelAdmin

from Enquestes.models import Rol


# Register your models here.
class RolAdmin(ModelAdmin):
    pass

admin.site.register(Rol, ModelAdmin)