from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic.base import View

from Enquestes.models import Rol, Questionari, Pregunte
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        # Mètode autenticate -> serveix per autenticar.
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

class LlistarRols(View):
    def get(self, request):
        context={
            "rols":
                list(Rol.objects.all()),
            "nomRols":
                ((0, 'Professor'), (1, 'Coordinador'))
        }
        return render(request, 'LlistarRols.html', context)

class RolsSeeder(View):
    def get(self, request, Nom):
        Rol.objects.create(nom = Nom)
        return HttpResponse(content = 'Prova')


class SeederUsuari(View):
    def get(self, request):
        # Veure la pàgina HTML https://docs.djangoproject.com/en/5.1/topics/auth/default/
        User.objects.create_user(username='prova1', password='super3', email='prova1@correu.cat')
        return HttpResponse(content='ok!')

class LlistarQuestionaris(View):
    def get(self, request):
        if request.GET.get('editar'):
            pass
        else:
            context = {
                "questionaris":
                    list(Questionari.objects.all())
            }
            return render(request, 'LlistarQuestionaris.html', context)

class EditarQuestionari(View):
    def get(self, request, id):
        # Falta posar tota la info de la id del qüestionari
        context = {
            "id":
                id
        }
        return render(request, 'EditarQuestionari.html', context)
        pass