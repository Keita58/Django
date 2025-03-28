from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator

# Create your views here.
from django.views.generic.base import View

from Enquestes.models import Questionari, Pregunte, Alumne, Resposte


@method_decorator(permission_required(perm='Coordinador'), name='get')
# Classes pels qüestionaris
class LlistarQuestionaris(View):
    def get(self, request):
        context = {
            "questionaris":
                list(Questionari.objects.all())
        }
        return render(request, 'LlistarQuestionaris.html', context)


@method_decorator(permission_required(perm='Coordinador'), name='get')
@method_decorator(permission_required(perm='Coordinador'), name='post')
class EditarQuestionari(View):
    def get(self, request, id):
        context = {
            "questionari":
                Questionari.objects.get(idQuestionaris=id)
        }
        return render(request, 'EditarQuestionari.html', context)

    def post(self, request, id):
        questionari = get_object_or_404(Questionari, idQuestionaris=id)
        questionari.idEmpresa = request.POST.get('idEmpresa')
        questionari.descripcio = request.POST.get('descripcio')
        questionari.save()
        return redirect('llistaQuestionaris')


@method_decorator(permission_required(perm='Coordinador'), name='get')
class EsborrarQuestionari(View):
    def get(self, request, id):
        questionari = Questionari.objects.get(idQuestionaris=id)
        questionari.delete()
        return redirect('llistaQuestionaris')


@method_decorator(permission_required(perm='Coordinador'), name='get')
@method_decorator(permission_required(perm='Coordinador'), name='post')
class CrearQuestionari(View):
    def get(self, request):
        return render(request, 'CrearQuestionari.html')

    def post(self, request):
        Questionari.objects.create(idEmpresa=request.POST.get('idEmpresa'), descripcio=request.POST.get('descripcio'))
        return redirect('llistaQuestionaris')


#Classes per les preguntes
@method_decorator(permission_required(perm='Coordinador'), name='get')
class LlistarPreguntes(View):
    def get(self, request):
        context = {
            "preguntes":
                list(Pregunte.objects.all())
        }
        return render(request, 'LlistarPreguntes.html', context)


@method_decorator(permission_required(perm='Coordinador'), name='get')
@method_decorator(permission_required(perm='Coordinador'), name='post')
class EditarPregunta(View):
    def get(self, request, id):
        context = {
            "pregunta":
                Pregunte.objects.get(idPreguntes=id),
            "questionaris":
                Questionari.objects.all()
        }
        return render(request, 'EditarPregunta.html', context)

    def post(self, request, id):
        pregunta = get_object_or_404(Pregunte, idPreguntes=id)
        pregunta.descripcio = request.POST.get('descripcio')
        questionari = Questionari.objects.get(idQuestionaris=request.POST.get('questionari'))
        pregunta.questionari = questionari
        pregunta.save()
        return redirect('llistaPreguntes')


@method_decorator(permission_required(perm='Coordinador'), name='get')
class EsborrarPregunta(View):
    def get(self, request, id):
        pregunta = Pregunte.objects.get(idPreguntes=id)
        pregunta.delete()
        return redirect('llistaPreguntes')


@method_decorator(permission_required(perm='Coordinador'), name='get')
@method_decorator(permission_required(perm='Coordinador'), name='post')
class CrearPregunta(View):
    def get(self, request):
        context = {
            "questionaris":
                list(Questionari.objects.all())
        }
        return render(request, 'CrearPregunta.html', context)

    def post(self, request):
        Pregunte.objects.create(descripcio=request.POST.get('descripcio'),
                                questionari=Questionari.objects.get(idQuestionaris=request.POST.get('questionari')))
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
                Alumne.objects.get(idAlumnes=id),
        }
        return render(request, 'EditarAlumne.html', context)

    def post(self, request, id):
        alumne = get_object_or_404(Alumne, idAlumnes=id)
        alumne.nomComplet = request.POST.get('nomComplet')
        alumne.questionari = request.POST.get('questionari')
        alumne.save()
        return redirect('llistaAlumnes')


class EsborrarAlumne(View):
    def get(self, request, id):
        alumne = Alumne.objects.get(idAlumnes=id)
        alumne.delete()
        return redirect('llistaAlumnes')


class CrearAlumne(View):
    def get(self, request):
        return render(request, 'CrearAlumne.html')

    def post(self, request):
        Alumne.objects.create(nomComplet=request.POST.get('nomComplet'), img=request.POST.get('img'),
                              questionari=request.POST.get('questionari'))
        return redirect('llistaAlumnes')


#Adreces compostes
class CreaRespostesQuestionari(View):
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


class RespondreRespostesQuestionari(View):
    def get(self, request):
        return render(request, 'RespondreRespostes.html')

    def post(self, request):
        respostes = []
        preguntes = Pregunte.objects.filter(questionari=request.POST.get("questionari"))
        for pregunta in preguntes:
            respostes.append(
                get_object_or_404(Resposte, idProfessor=get_object_or_404(User, id=request.POST.get("profe")),
                                  idAlumne=get_object_or_404(Alumne, idAlumnes=request.POST.get("alumne")),
                                  idPregunta=pregunta))
        context = {
            "respostes": respostes,
            "preguntes": preguntes
        }
        return render(request, 'RespondreRespostesForm.html', context)


class RespondreRespostesForm(View):
    def post(self, request):
        pass


class TancarQuestionariAlumne(View):
    def post(self, request):
        preguntes = Pregunte.objects.filter(questionari=request.POST.get("questionari"))
        for pregunta in preguntes:
            resposta = get_object_or_404(Resposte, idProfessor=get_object_or_404(User, id=request.POST.get("profe")),
                                         idAlumne=get_object_or_404(Alumne, idAlumnes=request.POST.get("alumne")),
                                         idPregunta=pregunta)
            resposta.tancar = True
            resposta.save()
        return render(request, 'TancarRespostesQuestionari.html')
