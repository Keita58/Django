from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.views.generic.base import View

from Enquestes.models import Rol, Questionari, Pregunte, Alumne


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


# Classes pels rols
class LlistarRols(View):
    def get(self, request):
        context={
            "rols":
                list(Rol.objects.all())
        }
        return render(request, 'LlistarRols.html', context)

class EditarRol(View):
    def get(self, request, id):
        context={
            "rol":
                Rol.objects.get(idRols = id),
        }
        return render(request, 'EditarRol.html', context)

    def post(self, request, id):
        rol = get_object_or_404(Rol, idRols = id)
        rol.nom = request.POST.get('nom')
        rol.save()
        return redirect('llistarRols')

class EsborrarRol(View):
    def get(self, request, id):
        rol = Rol.objects.get(idRols = id)
        rol.delete()
        return redirect('llistarRols')

class CrearRol(View):
    def get(self, request):
        return render(request, 'CrearRol.html')

    def post(self, request):
        Rol.objects.create(nom = request.POST.get('nom'))
        return redirect('llistarRols')


# Classes pels qüestionaris
class LlistarQuestionaris(View):
    def get(self, request):
        context = {
            "questionaris":
                list(Questionari.objects.all())
        }
        return render(request, 'LlistarQuestionaris.html', context)

class EditarQuestionari(View):
    def get(self, request, id):
        context = {
            "questionari":
                Questionari.objects.get(idQuestionaris = id)
        }
        return render(request, 'EditarQuestionari.html', context)

    def post(self, request, id):
        questionari = get_object_or_404(Questionari, idQuestionaris = id)
        questionari.idEmpresa = request.POST.get('idEmpresa')
        questionari.descripcio = request.POST.get('descripcio')
        questionari.save()
        return redirect('llistaQuestionaris')

class EsborrarQuestionari(View):
    def get(self, request, id):
        questionari = Questionari.objects.get(idQuestionaris = id)
        questionari.delete()
        return redirect('llistaQuestionaris')

class CrearQuestionari(View):
    def get(self, request):
        return render(request, 'CrearQuestionari.html')

    def post(self, request):
        Questionari.objects.create(idEmpresa = request.POST.get('idEmpresa'), descripcio = request.POST.get('descripcio'))
        return redirect('llistaQuestionaris')


#Classes per les preguntes
class LlistarPreguntes(View):
    def get(self, request):
        context = {
            "preguntes":
                list(Pregunte.objects.all())
        }
        return render(request, 'LlistarPreguntes.html', context)

class EditarPregunta(View):
    def get(self, request, id):
        context = {
            "pregunta":
                Pregunte.objects.get(idPreguntes = id),
            "questionaris":
                Questionari.objects.all()
        }
        return render(request, 'EditarPregunta.html', context)

    def post(self, request, id):
        pregunta = get_object_or_404(Pregunte, idPreguntes = id)
        pregunta.descripcio = request.POST.get('descripcio')
        questionari = Questionari.objects.get(idQuestionaris = request.POST.get('questionari'))
        pregunta.questionari = questionari
        pregunta.save()
        return redirect('llistaPreguntes')

class EsborrarPregunta(View):
    def get(self, request, id):
        pregunta = Pregunte.objects.get(idPreguntes = id)
        pregunta.delete()
        return redirect('llistaPreguntes')

class CrearPregunta(View):
    def get(self, request):
        context = {
            "questionaris":
                list(Questionari.objects.all())
        }
        return render(request, 'CrearPregunta.html', context)

    def post(self, request):
        Pregunte.objects.create(descripcio = request.POST.get('descripcio'), questionari = Questionari.objects.get(idQuestionaris = request.POST.get('questionari')))
        return redirect('llistaPreguntes')


#Classes pels alumnes
class LlistarAlumnes(View):
    def get(self, request):
        context = {
            "alumnes":
                list(Alumne.objects.all())
        }
        return render(request, 'LlistarAlumnes.html', context)

class EditarAlumne(View):
    def get(self, request, id):
        context = {
            "alumne":
                Alumne.objects.get(isAlumnes = id),
        }
        return render(request, 'EditarPregunta.html', context)

    def post(self, request, id):
        alumne = get_object_or_404(Alumne, idAlumnes = id)
        alumne.nomComplet = request.POST.get('nomComplet')
        alumne.img = request.POST.get('img')
        alumne.questionari = request.POST.get('questionari')
        alumne.save()
        return redirect('llistaAlumnes')

class EsborrarAlumne(View):
    def get(self, request, id):
        alumne = Alumne.objects.get(idAlumnes = id)
        alumne.delete()
        return redirect('llistaAlumnes')

class CrearAlumne(View):
    def get(self, request):
        return render(request, 'CrearAlumne.html')

    def post(self, request):
        Alumne.objects.create(nomComplet = request.POST.get('nomComplet'), img = request.POST.get('img'), questionari = request.POST.get('questionari'))
        return redirect('llistaAlumnes')
