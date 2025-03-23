from django.contrib import admin
from django.contrib.admin import ModelAdmin

from Enquestes.models import Rol, Questionari, Pregunte, Alumne


# Register your models here.
class RolAdmin(ModelAdmin):
    pass

class QuestionAdmin(ModelAdmin):
    pass

class PreguntesAdmin(ModelAdmin):
    pass

class AlumneAdmin(ModelAdmin):
    pass

admin.site.register(Rol, ModelAdmin)
admin.site.register(Questionari, RolAdmin)
admin.site.register(Pregunte, PreguntesAdmin)
admin.site.register(Alumne, AlumneAdmin)
