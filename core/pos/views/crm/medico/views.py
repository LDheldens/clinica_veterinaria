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
from core.pos.forms import ClientForm, User, Medico, MedicoForm
from core.security.mixins import ModuleMixin, PermissionMixin



class MedicoListView(PermissionMixin, TemplateView):
    template_name = 'crm/medico/list.html'
    permission_required = 'view_medico'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                for medico in Medico.objects.all():
                    data.append(medico.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('medico_create')
        context['title'] = 'Listado de Médicos'
        return context


class MedicoCreateView(PermissionMixin, CreateView):
    model = Medico
    template_name = 'crm/medico/create.html'
    form_class = MedicoForm
    success_url = reverse_lazy('medico_list')
    permission_required = 'add_medico'

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            if type == 'dni':
                if User.objects.filter(dni=obj):
                    data['valid'] = False
            elif type == 'mobile':
                if Medico.objects.filter(mobile=obj):
                    data['valid'] = False
            elif type == 'email':
                if User.objects.filter(email=obj):
                    data['valid'] = False
            elif type == 'codigo_medico':
                if Medico.objects.filter(codigo_medico=obj):
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

                    medico = Medico()
                    medico.user_id = user.id
                    medico.mobile = request.POST['mobile']
                    medico.especialidad = request.POST['especialidad']
                    medico.codigo_medico= request.POST['codigo_medico']
                    medico.save()

                    group = Group.objects.get(pk=settings.GROUPS.get('medic'))
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
        context['title'] = 'Nuevo registro de un Médico'
        context['action'] = 'add'
        context['instance'] = None
        return context

class MedicoUpdateView(PermissionMixin, UpdateView):
    model = Medico
    template_name = 'crm/medico/create.html'  # Reemplaza con el nombre de tu template de actualización
    form_class = MedicoForm
    success_url = reverse_lazy('medico_list')
    permission_required = 'change_medico'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        instance = self.object
        form = MedicoForm(instance=instance, initial={
            'first_name': instance.user.first_name,
            'last_name': instance.user.last_name,
            'dni': instance.user.dni,
            'email': instance.user.email,
            'image': instance.user.image,
            'mobile': instance.mobile,  # Agregamos el campo mobile
            'especialidad': instance.especialidad,  # Agregamos el campo especialidad
            'codigo_medico': instance.codigo_medico,  # Agregamos el campo especialidad
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
                if Medico.objects.filter(mobile=obj).exclude(id=instance.id):
                    data['valid'] = False
            elif type == 'email':
                if User.objects.filter(email=obj).exclude(id=instance.user.id):
                    data['valid'] = False
            elif type == 'codigo_medico':
                if Medico.objects.filter(codigo_medico=obj):
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

                    medico = instance
                    medico.user_id = user.id
                    medico.mobile = request.POST['mobile']
                    medico.especialidad = request.POST['especialidad']
                    medico.codigo_medico = request.POST['codigo_medico']
                    medico.save()
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
        context['title'] = 'Edición de un Médico'
        context['action'] = 'edit'
        context['instance'] = self.object
        return context

class MedicoDeleteView(PermissionMixin, DeleteView):
    model = Medico
    template_name = 'crm/medico/delete.html'
    success_url = reverse_lazy('medico_list')
    permission_required = 'delete_medico'

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