import json
from django.db.models import Q
from django.contrib.auth.models import Group
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView

from config import settings
from core.pos.forms import ClientForm, HospitalizacionForm, User, Client, TipoMascota, TipoMascotaForm, Paciente, PacienteForm, Hospitalizacion
from core.security.mixins import ModuleMixin, PermissionMixin

class TipoMascotaListView(PermissionMixin, TemplateView):
    template_name = 'crm/tipo_mascota/list.html'
    permission_required = 'view_client'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                for i in TipoMascota.objects.filter():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        print(data)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('tipo_mascota_create')
        context['title'] = 'Listado de mascotas'
        return context
    
class TipoMascotaCreateView(PermissionMixin, CreateView):
    model = TipoMascota
    template_name = 'crm/tipo_mascota/create.html'
    form_class = TipoMascotaForm
    success_url = reverse_lazy('tipo_mascota_list')
    permission_required = 'add_client'

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            if type == 'tipo_mascota':
                if TipoMascota.objects.filter(tipo_mascota=obj):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                with transaction.atomic():
                    tipo_mascota = TipoMascota()
                    tipo_mascota.tipo_mascota = request.POST['tipo_mascota']
                    tipo_mascota.save()
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un tipo de mascota'
        context['action'] = 'add'
        context['instance'] = None
        return context

class TipoMascotaUpdateView(PermissionMixin, UpdateView):
    model = TipoMascota
    template_name = 'crm/tipo_mascota/create.html'
    form_class = TipoMascotaForm
    success_url = reverse_lazy('tipo_mascota_list')
    permission_required = 'change_client'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        instance = self.object
        form = TipoMascotaForm(instance=instance, initial={
            'tipo_mascota': instance.tipo_mascota
        })
        return form

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            if type == 'tipo_mascota':
                if TipoMascota.objects.filter(tipo_mascota=obj):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                with transaction.atomic():
                    instance = self.object
                    tipo_mascota = instance
                    tipo_mascota.tipo_mascota = request.POST['tipo_mascota']
                    tipo_mascota.save()
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un tipo de mascota'
        context['action'] = 'edit'
        context['instance'] = self.object
        return context

class TipoMascotaDeleteView(PermissionMixin, DeleteView):
    model = TipoMascota
    template_name = 'crm/tipo_mascota/delete.html'
    success_url = reverse_lazy('tipo_mascota_list')
    permission_required = 'delete_client'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            with transaction.atomic():
                instance = self.get_object()
                instance.delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context


class HospitalizacionListView(PermissionMixin, TemplateView):
    template_name = 'crm/hospitalizacion/list.html'
    permission_required = 'view_client'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                for i in Hospitalizacion.objects.filter():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        print(data)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('hospitalizacion_create')
        context['title'] = 'Listado de Hospitalización'
        return context
    
class HospitalizacionCreateView(PermissionMixin, CreateView):
    model = Hospitalizacion
    template_name = 'crm/hospitalizacion/create.html'
    form_class = HospitalizacionForm
    success_url = reverse_lazy('hospitalizacion_list')
    permission_required = 'add_client'

    def validate_data(self):
        data = {'valid': True}
        try:
            mascota_id = self.request.POST['mascota']
            
            # Verificar si la mascota ya tiene una hospitalización activa
            if Hospitalizacion.objects.filter(Q(mascota_id=mascota_id) & Q(internado=True)).exists():
                data['valid'] = False
        except Exception as e:
            data['valid'] = False
            data['error'] = str(e)
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        print(request.POST)
        try:
            if action == 'add':
                with transaction.atomic():
                    print('XD SI DENTRO AL TOMIC')
                    hospitalizacion = Hospitalizacion()
                    hospitalizacion.mascota_id = request.POST['mascota']
                    hospitalizacion.fecha_ingreso = request.POST['fecha_ingreso']
                    hospitalizacion.fecha_salida = request.POST['fecha_salida']
                    hospitalizacion.medicinas_aplicadas = request.POST['medicinas_aplicadas']
                    hospitalizacion.motivo = request.POST['motivo']
                    print('HASTA AQUI')
                    hospitalizacion.antecedentes = request.POST['antecedentes']
                    hospitalizacion.tratamiento = request.POST['tratamiento']
                    hospitalizacion.save()
                    print('Hospitalización guardada:', hospitalizacion)
            elif action == 'add2':
                hospitalizacion = Hospitalizacion()
                hospitalizacion.mascota_id = request.POST['mascota']
                
                if Hospitalizacion.objects.filter(mascota_id=request.POST['mascota'], internado=True).exists():
                    data['error'] = 'La mascota ya está hospitalizada e internada.'
                    return JsonResponse(data)
                
                hospitalizacion.fecha_ingreso = request.POST['fecha_ingreso']
                hospitalizacion.fecha_salida = request.POST['fecha_salida']
                hospitalizacion.medicinas_aplicadas = request.POST['medicinas_aplicadas']
                hospitalizacion.motivo = request.POST['motivo']
                hospitalizacion.antecedentes = request.POST['antecedentes']
                hospitalizacion.tratamiento = request.POST['tratamiento']
                hospitalizacion.save()
                print('Hospitalización guardada:', hospitalizacion)
                
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de hospitalización'
        context['action'] = 'add'
        context['instance'] = None
        return context

class HospitalizacionUpdateView(PermissionMixin, UpdateView):
    model = Hospitalizacion
    template_name = 'crm/hospitalizacion/create.html'
    form_class = HospitalizacionForm
    success_url = reverse_lazy('hospitalizacion_list')
    permission_required = 'change_client'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        instance = self.object
        form = HospitalizacionForm(instance=instance, initial={
            'mascota': instance.mascota,
            'fecha_ingreso': instance.fecha_ingreso,
            'fecha_salida': instance.fecha_salida,
            'medicinas_aplicadas': instance.medicinas_aplicadas,
            'motivo': instance.motivo,
            'antecedentes': instance.antecedentes,
            'tratamiento': instance.tratamiento,
            'internado': instance.internado,
        })
        return form

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            if type == 'mascota':
                if Hospitalizacion.objects.filter(mascota_id=obj):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                with transaction.atomic():
                    instance = self.object
                    hospitalizacion = instance
                    hospitalizacion.mascota_id = request.POST['mascota']
                    hospitalizacion.fecha_ingreso = request.POST['fecha_ingreso']
                    hospitalizacion.fecha_salida = request.POST['fecha_salida']
                    hospitalizacion.medicinas_aplicadas = request.POST['medicinas_aplicadas']
                    hospitalizacion.motivo = request.POST['motivo']
                    hospitalizacion.antecedentes = request.POST['antecedentes']
                    hospitalizacion.tratamiento = request.POST['tratamiento']
                    hospitalizacion.internado = request.POST.get('internado', False) == 'on'
                    hospitalizacion.save()
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de una hospitalización'
        context['action'] = 'edit'
        context['instance'] = self.object
        return context

class HospitalizacionDeleteView(PermissionMixin, DeleteView):
    model = Hospitalizacion
    template_name = 'crm/hospitalizacion/delete.html'
    success_url = reverse_lazy('hospitalizacion_list')
    permission_required = 'delete_client'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            with transaction.atomic():
                instance = self.get_object()
                instance.delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context

class HospitalizacionUpdateInternamientoView(PermissionMixin, DeleteView):
    model = Hospitalizacion
    template_name = 'crm/hospitalizacion/udpate_internamiento.html'
    success_url = reverse_lazy('hospitalizacion_list')
    permission_required = 'delete_client'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            with transaction.atomic():
                instance = self.get_object()
                instance.internado = False if instance.internado else True
                instance.save()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de actualización de internamiento'
        context['list_url'] = self.success_url
        return context

class PacienteListView(PermissionMixin, TemplateView):
    template_name = 'crm/paciente/list.html'
    permission_required = 'view_paciente'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                for i in Paciente.objects.filter():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        print(data)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('paciente_create')
        context['title'] = 'Listado de Pacientes'
        return context
    
class PacienteCreateView(PermissionMixin, CreateView):
    model = Paciente
    template_name = 'crm/paciente/create.html'
    form_class = PacienteForm
    success_url = reverse_lazy('paciente_list')
    permission_required = 'add_paciente'

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            if type == 'identificacion':
                if Paciente.objects.filter(identificacion=obj):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                with transaction.atomic():
                    paciente = Paciente()
                    paciente.identificacion = request.POST['identificacion']
                    paciente.propietario_id = request.POST['propietario']
                    paciente.nombre = request.POST['nombre']
                    paciente.fecha_nacimiento = request.POST['fecha_nacimiento']
                    paciente.tipo_mascota_id = request.POST['tipo_mascota']
                    paciente.sexo = request.POST['sexo']
                    paciente.tamanio = request.POST['tamanio']
                    paciente.raza = request.POST['raza']
                    paciente.edad = request.POST['edad']
                    paciente.peso = request.POST['peso']
                    paciente.descripcion = request.POST['descripcion']
                    paciente.save()
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un paciente'
        context['action'] = 'add'
        context['instance'] = None
        return context

class PacienteUpdateView(PermissionMixin, UpdateView):
    model = Paciente
    template_name = 'crm/paciente/create.html'
    form_class = PacienteForm
    success_url = reverse_lazy('paciente_list')
    permission_required = 'change_paciente'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        instance = self.object
        form = PacienteForm(instance=instance, initial={
            'tipo_mascota': instance.tipo_mascota,
            'identificacion': instance.identificacion,
            'propietario': instance.propietario,
            'nombre': instance.nombre,
            'fecha_nacimiento': instance.fecha_nacimiento,
            'sexo': instance.sexo,
            'tamanio': instance.tamanio,
            'raza': instance.raza,
            'edad': instance.edad,
            'peso': instance.peso,
            'descripcion': instance.descripcion,
        })
        return form

    def validate_data(self):
        data = {'valid': True}
        # try:
        #     type = self.request.POST['type']
        #     obj = self.request.POST['obj'].strip()
        #     if type == 'identificacion':
        #         if Paciente.objects.filter(identificacion=obj):
        #             data['valid'] = False
        # except:
        #     pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        print(request)
        try:
            if action == 'edit':
                with transaction.atomic():
                    instance = self.object
                    paciente = instance
                    paciente.tipo_mascota_id = request.POST['tipo_mascota']
                    paciente.identificacion = request.POST['identificacion']
                    paciente.propietario_id = request.POST['propietario']
                    paciente.nombre = request.POST['nombre']
                    paciente.fecha_nacimiento = request.POST['fecha_nacimiento']
                    paciente.sexo = request.POST['sexo']
                    paciente.tamanio = request.POST['tamanio']
                    paciente.raza = request.POST['raza']
                    paciente.edad = request.POST['edad']
                    paciente.peso = request.POST['peso']
                    paciente.edad = request.POST['edad']
                    paciente.descripcion = request.POST['descripcion']
                    paciente.save()
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un paciente'
        context['action'] = 'edit'
        context['instance'] = self.object
        return context

class PacienteDeleteView(PermissionMixin, DeleteView):
    model = Paciente
    template_name = 'crm/paciente/delete.html'
    success_url = reverse_lazy('paciente_list')
    permission_required = 'delete_paciente'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            with transaction.atomic():
                instance = self.get_object()
                instance.delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context


class ClientListView(PermissionMixin, TemplateView):
    template_name = 'crm/client/list.html'
    permission_required = 'view_client'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                for i in Client.objects.filter():
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

class ClientCreateView(PermissionMixin, CreateView):
    model = Client
    template_name = 'crm/client/create.html'
    form_class = ClientForm
    success_url = reverse_lazy('client_list')
    permission_required = 'add_client'

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            if type == 'dni':
                if User.objects.filter(dni=obj):
                    data['valid'] = False
            elif type == 'mobile':
                if Client.objects.filter(mobile=obj):
                    data['valid'] = False
            elif type == 'email':
                if User.objects.filter(email=obj):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                with transaction.atomic():
                    user = User()
                    user.first_name = request.POST['first_name']
                    user.last_name = request.POST['last_name']
                    user.dni = request.POST['dni']
                    user.username = user.dni
                    if 'image' in request.FILES:
                        user.image = request.FILES['image']
                    user.create_or_update_password(user.dni)
                    user.email = request.POST['email']
                    user.save()

                    client = Client()
                    client.user_id = user.id
                    client.mobile = request.POST['mobile']
                    client.address = request.POST['address']
                    client.birthdate = request.POST['birthdate']
                    client.save()

                    group = Group.objects.get(pk=settings.GROUPS.get('client'))
                    user.groups.add(group)
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un Cliente'
        context['action'] = 'add'
        context['instance'] = None
        return context

class ClientUpdateView(PermissionMixin, UpdateView):
    model = Client
    template_name = 'crm/client/create.html'
    form_class = ClientForm
    success_url = reverse_lazy('client_list')
    permission_required = 'change_client'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        instance = self.object
        form = ClientForm(instance=instance, initial={
            'first_name': instance.user.first_name,
            'last_name': instance.user.last_name,
            'dni': instance.user.dni,
            'email': instance.user.email,
            'image': instance.user.image,
        })
        return form

    def validate_data(self):
        data = {'valid': True}
        try:
            instance = self.object
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            if type == 'dni':
                if User.objects.filter(dni=obj).exclude(id=instance.user.id):
                    data['valid'] = False
            elif type == 'mobile':
                if Client.objects.filter(mobile=obj).exclude(id=instance.id):
                    data['valid'] = False
            elif type == 'email':
                if User.objects.filter(email=obj).exclude(id=instance.user.id):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                with transaction.atomic():
                    instance = self.object
                    user = instance.user
                    user.first_name = request.POST['first_name']
                    user.last_name = request.POST['last_name']
                    user.dni = request.POST['dni']
                    user.username = user.dni
                    if 'image-clear' in request.POST:
                        user.remove_image()
                    if 'image' in request.FILES:
                        user.image = request.FILES['image']
                    user.email = request.POST['email']
                    user.save()

                    client = instance
                    client.user_id = user.id
                    client.mobile = request.POST['mobile']
                    client.address = request.POST['address']
                    client.birthdate = request.POST['birthdate']
                    client.save()
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un Cliente'
        context['action'] = 'edit'
        context['instance'] = self.object
        return context

class ClientDeleteView(PermissionMixin, DeleteView):
    model = Client
    template_name = 'crm/client/delete.html'
    success_url = reverse_lazy('client_list')
    permission_required = 'delete_client'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            with transaction.atomic():
                instance = self.get_object()
                user = instance.user
                instance.delete()
                user.delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context

class ClientUpdateProfileView(ModuleMixin, UpdateView):
    model = Client
    template_name = 'crm/client/profile.html'
    form_class = ClientForm
    success_url = reverse_lazy('dashboard')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user.client

    def get_form(self, form_class=None):
        instance = self.object
        form = ClientForm(instance=instance, initial={
            'first_name': instance.user.first_name,
            'last_name': instance.user.last_name,
            'dni': instance.user.dni,
            'email': instance.user.email,
            'image': instance.user.image,
        })
        return form

    def validate_data(self):
        data = {'valid': True}
        try:
            instance = self.object
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            if type == 'dni':
                if User.objects.filter(dni=obj).exclude(id=instance.user.id):
                    data['valid'] = False
            elif type == 'mobile':
                if Client.objects.filter(mobile=obj).exclude(id=instance.id):
                    data['valid'] = False
            elif type == 'email':
                if User.objects.filter(email=obj).exclude(id=instance.user.id):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                with transaction.atomic():
                    instance = self.object
                    user = instance.user
                    user.first_name = request.POST['first_name']
                    user.last_name = request.POST['last_name']
                    user.dni = request.POST['dni']
                    user.username = user.dni
                    if 'image-clear' in request.POST:
                        user.remove_image()
                    if 'image' in request.FILES:
                        user.image = request.FILES['image']
                    user.email = request.POST['email']
                    user.save()

                    client = instance
                    client.user_id = user.id
                    client.mobile = request.POST['mobile']
                    client.address = request.POST['address']
                    client.birthdate = request.POST['birthdate']
                    client.save()
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de Perfil'
        context['action'] = 'edit'
        context['instance'] = self.object
        return context
