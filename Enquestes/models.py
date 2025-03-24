from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.db.models import ManyToManyField


# Create your models here.

def django_enum(cls):
    # decorator needed to enable enums in django templates
    cls.do_not_call_in_templates = True
    return cls

class Questionari(models.Model):
    idQuestionaris = models.AutoField(primary_key=True)
    idEmpresa = models.IntegerField('idEmpresa')
    descripcio = models.CharField('descripcio', max_length=255)
    def __str__(self):
        return str(self.idQuestionaris)

class Pregunte(models.Model):
    idPreguntes = models.AutoField(primary_key=True)
    descripcio = models.CharField('descripcio', max_length=255)
    questionari = models.ForeignKey(Questionari, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.idPreguntes)

class Alumne(models.Model):
    idAlumnes = models.AutoField(primary_key=True)
    nomComplet = models.CharField('nomComplet', max_length=255)
    questionari = models.BooleanField(default=False)
    preguntes = ManyToManyField(Pregunte, through="Resposte")
    professors = ManyToManyField(User, through="Resposte")
    def __str__(self):
        return str(self.idAlumnes)

class Resposte(models.Model):
    idRespostes = models.AutoField(primary_key=True)
    valoracio = models.IntegerField()
    tancar = models.BooleanField(default=False)
    idProfessor = models.ForeignKey(User, on_delete=models.CASCADE)
    idPregunta = models.ForeignKey(Pregunte, on_delete=models.CASCADE)
    idAlumne = models.ForeignKey(Alumne, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.idRespostes)