"""
URL configuration for Django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from Enquestes.views import LlistarQuestionaris, \
    EditarQuestionari, EsborrarQuestionari, CrearQuestionari, LlistarPreguntes, \
    EditarPregunta, EsborrarPregunta, CrearPregunta, LlistarAlumnes, EditarAlumne, EsborrarAlumne, CrearAlumne, \
    CreaRespostesQuestionari, RespondreRespostesQuestionari, TancarQuestionariAlumne, RespondreRespostesForm, \
    SensePermisos
from users.views import LoginView, LogoutView

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    path('questionarilist/', LlistarQuestionaris.as_view(), name='llistaQuestionaris'),
    path('questionari/edit/<int:id>', EditarQuestionari.as_view(), name='editarQuestionari'),
    path('questionari/borrar/<int:id>', EsborrarQuestionari.as_view(), name='esborrarQuestionari'),
    path('questionari/add', CrearQuestionari.as_view(), name='crearQuestionari'),
    path('preguntalist/', LlistarPreguntes.as_view(), name='llistaPreguntes'),
    path('pregunta/edit/<int:id>', EditarPregunta.as_view(), name='editarPregunta'),
    path('pregunta/borrar/<int:id>', EsborrarPregunta.as_view(), name='esborrarPregunta'),
    path('pregunta/add', CrearPregunta.as_view(), name='crearPregunta'),
    path('alumneslist/', LlistarAlumnes.as_view(), name='llistaAlumnes'),
    path('alumne/edit/<int:id>', EditarAlumne.as_view(), name='editarAlumne'),
    path('alumne/borrar/<int:id>', EsborrarAlumne.as_view(), name='esborrarAlumne'),
    path('alumne/add', CrearAlumne.as_view(), name='crearAlumne'),
    # Adreces compostes
    path('preguntaalumne', CreaRespostesQuestionari.as_view(), name='creaRespostesQuestionari'),
    path('alumneresposta', RespondreRespostesQuestionari.as_view(), name='respondreRespostesQuestionari'),
    path('alumnequestionaritancar', TancarQuestionariAlumne.as_view(), name='tancarQuestionariAlumne'),
    path('respondrerespostes/<int:idAlumne>/<int:idQuestionari>/<int:idProfe>', RespondreRespostesForm.as_view(), name='respondreRespostesForm'),
    path('sensepermisos/', SensePermisos.as_view(), name='sensePermisos'),
]
