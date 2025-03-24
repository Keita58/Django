from django.contrib import admin
from django.contrib.admin import ModelAdmin

from Enquestes.models import Questionari, Pregunte, Alumne


# Register your models here.
class QuestionAdmin(ModelAdmin):
    pass

class PreguntesAdmin(ModelAdmin):
    pass

class AlumneAdmin(ModelAdmin):
    pass

class UsuariAdmin(ModelAdmin):
    pass

admin.site.register(Questionari, QuestionAdmin)
admin.site.register(Pregunte, PreguntesAdmin)
admin.site.register(Alumne, AlumneAdmin)
