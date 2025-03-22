from django.db import models

# Create your models here.
Rols = ((0, 'Professor'), (1, 'Coordinador'))

def django_enum(cls):
    # decorator needed to enable enums in django templates
    cls.do_not_call_in_templates = True
    return cls

class Rol(models.Model):
    idRols = models.AutoField(primary_key=True)
    nom = models.IntegerField(choices=Rols)
    models.Model.do_not_call_in_templates = True
    def __str__(self):
        return str(self.idRols)

class Questionaris(models.Model):
    idQuestionaris = models.AutoField(primary_key=True)
    idEmpresa = models.IntegerField('idEmpresa')
    descripcio = models.CharField('descripcio', max_length=255)
    def __str__(self):
        return str(self.idQuestionaris)

class Preguntes(models.Model):
    idPreguntes = models.AutoField(primary_key=True)
    descripcio = models.CharField('descripcio', max_length=255)
    questionari = models.ForeignKey(Questionaris, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.idPreguntes)

class Alumnes(models.Model):
    idAlumnes = models.AutoField(primary_key=True)
    nomComplet = models.CharField('nomComplet', max_length=255)
    img = models.CharField('img', max_length=255)
    questionari = models.BooleanField(default=False)
    def __str__(self):
        return str(self.idAlumnes)

