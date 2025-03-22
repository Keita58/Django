from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic.base import View

from Enquestes.models import Rol, Questionaris, Preguntes


class Enquestes(View):
    def get(self, data):
        return HttpResponse(content = 'Prova')

class RolsSeeder(View):
    def get(self, request, Nom):
        Rol.objects.create(nom = Nom)
        return HttpResponse(content = 'Prova')

class LlistarRols(View):
    def get(self, request):
        context={
            "rols":
                list(Rol.objects.all())
        }
        return render(request, 'LlistarRols.html', context)

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')
    def post(self, request):
        # Mètode autenticate -> serveix per autenciar.
        # Ell mateix encritpta i desencripta la credencial
        print (request.POST.get("username"))
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        # Comprovem que existeix un usuari
        print (user)
        if user is not None:
            # Mètode de django que obre una sessió d'usuari
            login(request, user)
            return HttpResponse(content='Success')
        # Fem aquest return per permetre tornar a fer login
        return self.get(request)
class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect('Enquestes:login')

class SeederUsuari(View):
    def get(self, request):
        # Veure la pàgina HTML https://docs.djangoproject.com/en/5.1/topics/auth/default/
        User.objects.create_user(username='prova1', password='super3', email='prova1@correu.cat')
        return HttpResponse(content='ok!')



