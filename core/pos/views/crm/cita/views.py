import json
from django.contrib import messages
from django.shortcuts import redirect,render
from django.http import HttpRequest, JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import Group
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView, View

from config import settings
from core.pos.forms import ClientForm, User, Client, Cita, CitaForm, Paciente
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
        context['create_url'] = reverse_lazy('cita_create')
        context['title'] = 'Listado de Citas'
        return context


class CitaCreateView(PermissionMixin, CreateView):
    model = Cita
    template_name = 'crm/cita/create.html'
    form_class = CitaForm
    success_url = reverse_lazy('cita_list')
    permission_required = 'add_cita'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                with transaction.atomic():
                    # Validar datos antes de crear la cita
                    validation_result = self.validate_data()
                    if not validation_result['valid']:
                        return JsonResponse(validation_result)

                    # Crear la instancia de Cita y asignar los campos
                    cita = Cita()
                    cita.medico_id = request.POST['medico']
                    cita.asunto = request.POST['asunto']
                    cita.descripcion = request.POST['descripcion']
                    cita.fecha_cita = request.POST['fecha_cita']
                    cita.hora_cita = request.POST['hora_cita']
                    cita.propietario_id = request.POST['propietario']
                    cita.mascota_id = request.POST['mascota']
                    cita.save()
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def validate_data(self):
        data = {'valid': True}
        try:
            fecha_cita = self.request.POST['fecha_cita']
            hora_cita = self.request.POST['hora_cita']
            medico = self.request.POST['medico']

            # Verificar si hay una cita previa con la misma fecha, hora y médico
            citas_en_mismo_horario = Cita.objects.filter(
                medico_id=medico,
                fecha_cita=fecha_cita,
                hora_cita=hora_cita
            ).exists()

            if citas_en_mismo_horario:
                data['valid'] = False
                data['error'] = 'Ya existe una cita programada para este médico en la misma fecha y hora.'
        except Exception as e:
            data['valid'] = False
            data['error'] = str(e)
        return data

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
    permission_required = 'change_cita'


    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'update':
                with transaction.atomic():
                    # Validar datos antes de actualizar la cita
                    validation_result = self.validate_data()
                    if not validation_result['valid']:
                        return JsonResponse(validation_result)

                    # Actualizar la instancia de Cita y asignar los campos
                    cita = self.get_object()  # Aquí se obtiene la instancia de la cita
                    cita.medico_id = request.POST['medico']
                    cita.asunto = request.POST['asunto']
                    cita.descripcion = request.POST['descripcion']
                    cita.fecha_cita = request.POST['fecha_cita']
                    cita.hora_cita = request.POST['hora_cita']
                    cita.propietario_id = request.POST['propietario']
                    cita.mascota_id = request.POST['mascota']
                    cita.save()
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def validate_data(self):
        data = {'valid': True}
        try:
            fecha_cita = self.request.POST['fecha_cita']
            hora_cita = self.request.POST['hora_cita']
            medico = self.request.POST['medico']

            # Verificar si hay una cita previa con la misma fecha, hora y médico
            citas_en_mismo_horario = Cita.objects.filter(
                medico_id=medico,
                fecha_cita=fecha_cita,
                hora_cita=hora_cita
            ).exclude(pk=self.kwargs['pk']).exists()  # Excluir la cita actual en la validación

            if citas_en_mismo_horario:
                data['valid'] = False
                data['error'] = 'Ya existe una cita programada para este médico en la misma fecha y hora.'
        except Exception as e:
            data['valid'] = False
            data['error'] = str(e)
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = self.success_url
        context['title'] = 'Editar cita'
        context['action'] = 'update'
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
    
class CambiarEstadoCitaView(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        cita_id = data.get('cita_id')
        try:
            cita = Cita.objects.get(pk=cita_id)
            cita.estado = not cita.estado
            cita.save()
            return JsonResponse({'message': 'Estado de la cita cambiado exitosamente'})
        except Cita.DoesNotExist:
            return JsonResponse({'error': 'La cita especificada no existe'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)



# registros manejados desde javascript
class RegistroCitaView(View):
    def post(self, request, *args, **kwargs):
        # Obtener los datos del formulario
        medico_id = request.POST.get('doctor')
        asunto = request.POST.get('asunto')
        descripcion = request.POST.get('descripcion')
        fecha_cita = request.POST.get('fecha')
        hora_cita = request.POST.get('hora')
        propietario_id = request.POST.get('propietario')
        paciente_id = request.POST.get('mascota')

        # Verificar si hay citas existentes para el médico en la misma fecha y hora
        citas_existente = Cita.objects.filter(
            medico_id=medico_id,
            fecha_cita=fecha_cita,
            hora_cita=hora_cita
        ).exists()

        if citas_existente:
            # Si hay citas existentes en la misma fecha y hora, devolver un error
            return JsonResponse({'error': 'Ya existe una cita registrada para este horario.'}, status=400)
        else:
            # Crear la cita
            cita = Cita.objects.create(
                medico_id=medico_id,
                asunto=asunto,
                descripcion=descripcion,
                fecha_cita=fecha_cita,
                hora_cita=hora_cita,
                propietario_id=propietario_id,
                mascota_id=paciente_id
            )

            # Retornar una respuesta JSON
            return JsonResponse({'mensaje': 'Cita registrada correctamente', 'id_cita': cita.id})

class EditarCitaView(View):
    def post(self, request, cita_id, *args, **kwargs):
        # Obtener la cita a editar
        cita = get_object_or_404(Cita, id=cita_id)

        # Obtener los datos actualizados del formulario
        medico_id = request.POST.get('doctor')
        asunto = request.POST.get('asunto')
        descripcion = request.POST.get('descripcion')
        fecha_cita = request.POST.get('fecha')
        hora_cita = request.POST.get('hora')
        propietario_id = request.POST.get('propietario')
        paciente_id = request.POST.get('mascota')

        # Verificar si hay citas existentes para el médico en la misma fecha y hora
        citas_existente = Cita.objects.filter(
            medico_id=medico_id,
            fecha_cita=fecha_cita,
            hora_cita=hora_cita
        ).exclude(id=cita_id).exists()

        if citas_existente:
            # Si hay citas existentes en la misma fecha y hora, devolver un error
            return JsonResponse({'error': 'Ya existe una cita registrada para este horario.'}, status=400)
        else:
            # Actualizar la cita
            cita.medico_id = medico_id
            cita.asunto = asunto
            cita.descripcion = descripcion
            cita.fecha_cita = fecha_cita
            cita.hora_cita = hora_cita
            cita.propietario_id = propietario_id
            cita.mascota_id = paciente_id
            cita.save()

            # Retornar una respuesta JSON
            return JsonResponse({'mensaje': 'Cita actualizada correctamente','id_cita': cita.id})
        
class EliminarCitaView(View):
    def post(self, request, cita_id, *args, **kwargs):
        # Buscar la cita por su ID
        try:
            cita = Cita.objects.get(pk=cita_id)
        except Cita.DoesNotExist:
            return JsonResponse({'error': 'La cita especificada no existe'}, status=404)
        
        # Eliminar la cita
        cita.delete()

        # Retornar una respuesta JSON
        return JsonResponse({'mensaje': 'Cita eliminada correctamente'})

class CargarMascotasView(View):
    def get(self, request, *args, **kwargs):
        propietario_id = request.GET.get('propietario_id')
        mascotas = Paciente.objects.filter(propietario_id=propietario_id)
        mascotas_data = [{'id': mascota.id, 'nombre': mascota.nombre} for mascota in mascotas]
        return JsonResponse({'mascotas': mascotas_data})