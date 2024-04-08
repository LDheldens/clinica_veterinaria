import json
from django.contrib import messages
from django.shortcuts import redirect,render
from django.http import HttpRequest, JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import Group
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView

from config import settings
from core.pos.forms import ClientForm, User, Client, Cita, CitaForm
from core.security.mixins import ModuleMixin, PermissionMixin


class CitaListView(PermissionMixin, TemplateView):
    template_name = 'crm/cita/list.html'
    permission_required = 'view_client'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                for i in Cita.objects.filter():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('client_create')
        context['title'] = 'Listado de Clientes'
        return context


class CitaCreateView(PermissionMixin, CreateView):
    model = Cita
    template_name = 'crm/cita/create.html'
    form_class = CitaForm
    success_url = reverse_lazy('cita_list')
    permission_required = 'add_client'

    def post(self, request, *args, **kwargs):
        form = CitaForm(request.POST, request.FILES)
        if form.is_valid():
            # Realizar la validación del cruce de citas aquí
            fecha_cita = form.cleaned_data['fecha_cita']
            hora_cita = form.cleaned_data['hora_cita']
            medico = form.cleaned_data['medico']

            # Verificar si hay una cita previa con la misma fecha, hora y médico
            citas_en_mismo_horario = Cita.objects.filter(
                medico=medico,
                fecha_cita=fecha_cita,
                hora_cita=hora_cita
            ).exists()

            if citas_en_mismo_horario:
                messages.error(request, "El médico ya tiene otra cita programada para este horario.")
                return render(request, self.template_name, {'form': form})

            form.save()
            return HttpResponseRedirect(self.success_url)
        else:
            # Si el formulario no es válido, mostrar solo el mensaje de cruce de horario en el template
            error_messages = form.errors.get('__all__', [])
            if "El médico ya tiene otra cita programada para este horario." in error_messages:
                messages.error(request, "El médico ya tiene otra cita programada para este horario.")
            return render(request, self.template_name, {'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de cita'
        context['action'] = 'add'
        context['instance'] = None
        return context

class CitaUpdateView(PermissionMixin, UpdateView):
    model = Cita
    template_name = 'crm/cita/create.html'
    form_class = CitaForm
    success_url = reverse_lazy('cita_list')
    permission_required = 'change_client'
    
    def post(self, request, *args, **kwargs):
        instance = self.get_object()  # Obtener la instancia existente a actualizar
        form = CitaForm(request.POST, request.FILES, instance=instance)  # Pasar la instancia al formulario
        if form.is_valid():
            # Realizar la validación del cruce de citas aquí
            fecha_cita = form.cleaned_data['fecha_cita']
            hora_cita = form.cleaned_data['hora_cita']
            medico = form.cleaned_data['medico']

            # Excluir la instancia actual de la consulta
            citas_en_mismo_horario = Cita.objects.filter(
                medico=medico,
                fecha_cita=fecha_cita,
                hora_cita=hora_cita
            ).exclude(id=instance.id).exists()

            if citas_en_mismo_horario:
                messages.error(request, "El médico ya tiene otra cita programada para este horario.")
                return render(request, self.template_name, {'form': form})

            form.save()
            return HttpResponseRedirect(self.success_url)
        else:
            # Si el formulario no es válido, mostrar los mensajes de error
            return render(request, self.template_name, {'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = self.success_url
        context['title'] = 'Actualización de cita'
        context['action'] = 'update'
        context['instance'] = None
        return context

class CitaDeleteView(PermissionMixin, DeleteView):
    model = Cita
    template_name = 'crm/cita/delete.html'
    success_url = reverse_lazy('cita_list')
    permission_required = 'delete_client'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.get_object().delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context