from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from Enquestes.models import Resposte, Questionari, Pregunte


# Create your views here.
class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.groups.filter(name='Professor').exists():
                respostes = Resposte.objects.filter(tancar=0)
                print(respostes)
                preguntes = []
                for i in range(len(respostes)):
                    aux = get_object_or_404(Pregunte, idPreguntes=respostes[i].idPregunta.idPreguntes)
                    if aux not in preguntes:
                        preguntes.append(aux)

                questionaris = []
                for i in range(len(preguntes)):
                    aux = get_object_or_404(Questionari, idQuestionaris = preguntes[i].questionari.idQuestionaris)
                    if aux not in questionaris:
                        questionaris.append(aux)

                context = {
                    "questionaris": questionaris,
                    "respostes": respostes,
                    "preguntes": preguntes
                }
                return render(request, 'Inici.html', context)
            else:
                context = {
                    "questionaris": Questionari.objects.all(),
                    "respostes": Resposte.objects.all(),
                    "preguntes": Pregunte.objects.all()
                }
                return render(request, 'Inici.html', context)
        else:
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
            return redirect('login')
        # Fem aquest return per permetre tornar a fer login
        return self.get(request)

class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect('login')
