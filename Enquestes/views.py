from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator

# Create your views here.
from django.views.generic.base import View

from Enquestes.models import Questionari, Pregunte, Alumne, Resposte


# Classes pels qüestionaris
class LlistarQuestionaris(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.groups.filter(name="Coordinador").exists():
            context = {
                "questionaris":
                    list(Questionari.objects.all())
            }
            return render(request, 'LlistarQuestionaris.html', context)
        else:
            return redirect('sensePermisos')


class EditarQuestionari(LoginRequiredMixin, View):
    def get(self, request, id):
        if request.user.groups.filter(name="Coordinador").exists():
            context = {
                "questionari":
                    Questionari.objects.get(idQuestionaris=id)
            }
            return render(request, 'EditarQuestionari.html', context)
        else:
            return redirect('sensePermisos')

    def post(self, request, id):
        if request.user.groups.filter(name="Coordinador").exists():
            questionari = get_object_or_404(Questionari, idQuestionaris=id)
            questionari.idEmpresa = request.POST.get('idEmpresa')
            questionari.descripcio = request.POST.get('descripcio')
            questionari.save()
            return redirect('llistaQuestionaris')
        else:
            return redirect('sensePermisos')


class EsborrarQuestionari(LoginRequiredMixin, View):
    def get(self, request, id):
        if request.user.groups.filter(name="Coordinador").exists():
            questionari = Questionari.objects.get(idQuestionaris=id)
            questionari.delete()
            return redirect('llistaQuestionaris')
        else:
            return redirect('sensePermisos')


class CrearQuestionari(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.groups.filter(name="Coordinador").exists():
            return render(request, 'CrearQuestionari.html')
        else:
            return redirect('sensePermisos')

    def post(self, request):
        if request.user.groups.filter(name="Coordinador").exists():
            Questionari.objects.create(idEmpresa=request.POST.get('idEmpresa'), descripcio=request.POST.get('descripcio'))
            return redirect('llistaQuestionaris')
        else:
            return redirect('sensePermisos')


#Classes per les preguntes
class LlistarPreguntes(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.groups.filter(name="Coordinador").exists():
            context = {
                "preguntes":
                    list(Pregunte.objects.all())
            }
            return render(request, 'LlistarPreguntes.html', context)
        else:
            return redirect('sensePermisos')


class EditarPregunta(LoginRequiredMixin, View):
    def get(self, request, id):
        if request.user.groups.filter(name="Coordinador").exists():
            context = {
                "pregunta":
                    Pregunte.objects.get(idPreguntes=id),
                "questionaris":
                    Questionari.objects.all()
            }
            return render(request, 'EditarPregunta.html', context)
        else:
            return redirect('sensePermisos')

    def post(self, request, id):
        if request.user.groups.filter(name="Coordinador").exists():
            pregunta = get_object_or_404(Pregunte, idPreguntes=id)
            pregunta.descripcio = request.POST.get('descripcio')
            questionari = Questionari.objects.get(idQuestionaris=request.POST.get('questionari'))
            pregunta.questionari = questionari
            pregunta.save()
            return redirect('llistaPreguntes')
        else:
            return redirect('sensePermisos')

class EsborrarPregunta(LoginRequiredMixin, View):
    def get(self, request, id):
        if request.user.groups.filter(name="Coordinador").exists():
            pregunta = Pregunte.objects.get(idPreguntes=id)
            pregunta.delete()
            return redirect('llistaPreguntes')
        else:
            return redirect('sensePermisos')


class CrearPregunta(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.groups.filter(name="Coordinador").exists():
            context = {
                "questionaris":
                    list(Questionari.objects.all())
            }
            return render(request, 'CrearPregunta.html', context)
        else:
            return redirect('sensePermisos')

    def post(self, request):
        if request.user.groups.filter(name="Coordinador").exists():
            Pregunte.objects.create(descripcio=request.POST.get('descripcio'),
                                    questionari=Questionari.objects.get(idQuestionaris=request.POST.get('questionari')))
            return redirect('llistaPreguntes')
        else:
            return redirect('sensePermisos')


#Classes pels alumnes
class LlistarAlumnes(LoginRequiredMixin, View):
    def get(self, request):
        context = {
            "alumnes":
                list(Alumne.objects.all())
        }
        return render(request, 'LlistarAlumnes.html', context)


class EditarAlumne(LoginRequiredMixin, View):
    def get(self, request, id):
        context = {
            "alumne":
                Alumne.objects.get(idAlumnes=id),
        }
        return render(request, 'EditarAlumne.html', context)

    def post(self, request, id):
        alumne = get_object_or_404(Alumne, idAlumnes=id)
        alumne.nomComplet = request.POST.get('nomComplet')
        alumne.questionari = request.POST.get('questionari')
        alumne.save()
        return redirect('llistaAlumnes')


class EsborrarAlumne(LoginRequiredMixin, View):
    def get(self, request, id):
        alumne = Alumne.objects.get(idAlumnes=id)
        alumne.delete()
        return redirect('llistaAlumnes')


class CrearAlumne(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'CrearAlumne.html')

    def post(self, request):
        Alumne.objects.create(nomComplet=request.POST.get('nomComplet'), img=request.POST.get('img'),
                              questionari=request.POST.get('questionari'))
        return redirect('llistaAlumnes')


#Adreces compostes
class CreaRespostesQuestionari(LoginRequiredMixin, View):
    def get(self, request):
        context = {
            "alumnes": Alumne.objects.all(),
            "questionaris": Questionari.objects.all(),
            "profes": User.objects.all()
        }
        return render(request, 'CreaRespostes.html', context)

    def post(self, request):
        preguntes = Pregunte.objects.filter(questionari=request.POST.get("questionari"))
        for pregunta in preguntes:
            Resposte.objects.create(idProfessor=get_object_or_404(User, id=request.POST.get("profe")),
                                    idAlumne=get_object_or_404(Alumne, idAlumnes=request.POST.get("alumne")),
                                    idPregunta=pregunta, valoracio=0)
        return redirect('creaRespostesQuestionari')


class RespondreRespostesQuestionari(LoginRequiredMixin, View):
    def get(self, request):
        context = {
            "alumnes": Alumne.objects.all(),
            "questionaris": Questionari.objects.all(),
            "profes": User.objects.all()
        }
        return render(request, 'RespondreRespostes.html', context)

    def post(self, request):
        respostes = []
        preguntes = Pregunte.objects.filter(questionari=request.POST.get("questionari"))
        preguntesHtml = []
        for pregunta in preguntes:
            respostes.append(
                get_object_or_404(Resposte, idProfessor=get_object_or_404(User, id=request.POST.get("profe")),
                                  idAlumne=get_object_or_404(Alumne, idAlumnes=request.POST.get("alumne")),
                                  idPregunta=pregunta))
            preguntesHtml.append(pregunta)
        context = {
            "respostes": respostes,
            "preguntes": preguntesHtml,
            "idalumne": request.POST.get("alumne"),
            "idquestionari": request.POST.get("questionari"),
            "idprofe": request.POST.get("profe"),
        }
        return render(request, 'RespondreRespostesForm.html', context)


class RespondreRespostesForm(LoginRequiredMixin, View):
    def post(self, request, idAlumne, idQuestionari, idProfe):
        preguntes = Pregunte.objects.filter(questionari=idQuestionari)
        for pregunta in preguntes:
            resposta = get_object_or_404(Resposte, idProfessor=get_object_or_404(User, id=idProfe),
                                         idAlumne=get_object_or_404(Alumne, idAlumnes=idAlumne),
                                         idPregunta=pregunta)
            resposta.valoracio = request.POST.get("valoracio"+str(pregunta))
            resposta.save()
        return redirect('respondreRespostesQuestionari')



class TancarQuestionariAlumne(LoginRequiredMixin, View):
    def get(self, request):
        context = {
            "alumnes": Alumne.objects.all(),
            "questionaris": Questionari.objects.all(),
            "profes": User.objects.all()
        }
        return render(request, 'TancarRespostesQuestionari.html', context)

    def post(self, request):
        preguntes = Pregunte.objects.filter(questionari=request.POST.get("questionari"))
        for pregunta in preguntes:
            resposta = get_object_or_404(Resposte, idProfessor=get_object_or_404(User, id=request.POST.get("profe")),
                                         idAlumne=get_object_or_404(Alumne, idAlumnes=request.POST.get("alumne")),
                                         idPregunta=pregunta)
            resposta.tancar = True
            resposta.save()
        return redirect('tancarQuestionariAlumne')

#Error: sense permisos
class SensePermisos(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'SensePermisos.html')