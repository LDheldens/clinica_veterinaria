import json
from django.db.models import F, Value
from django.db.models.functions import Concat
from django.contrib.auth.models import Group
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView, View, ListView

from config import settings
from core.pos.forms import ClientForm, User, Client, TipoMascota, Cita,TipoMascotaForm, Paciente, PacienteForm, Medico
from core.security.mixins import ModuleMixin, PermissionMixin

class CalendarioListView(TemplateView):
    template_name = 'crm/calendario/index.html'
    queryset = Cita.objects.none()  # Define un queryset vacío

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Calendario de Citas'
        return context

class ListaCitasView(TemplateView):
    def get(self, request, *args, **kwargs):
        citas = Cita.objects.all()
        eventos = [cita.toJSON() for cita in citas]
        return JsonResponse(eventos, safe=False)

class ObtenerDatosView(View):
    def get(self, request, *args, **kwargs):
        # Obtener datos de los médicos
        medicos = list(Medico.objects.all().values('id', 'user__first_name', 'user__last_name'))

        pacientes = list(Paciente.objects.all().annotate(nombre_completo=Concat('nombre', Value(' / '), 'tipo_mascota__tipo_mascota', Value(' / '), 'raza')).values('id', 'nombre_completo'))
        # Obtener datos de los clientes
        clientes = list(Client.objects.all().values('id', 'user__first_name', 'user__last_name'))

        # Devolver los datos en un solo JSON
        data = {
            'medicos': medicos,
            'pacientes': pacientes,
            'clientes': clientes
        }

        return JsonResponse(data)