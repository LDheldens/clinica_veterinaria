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
    object = None
    
    def post(self, request, *args, **kwargs):
        form = MedicoForm(request.POST,request.FILES)
        if form.is_valid():
            dni = form.cleaned_data['dni']
            if User.objects.filter(dni=dni).exists():
            # Si ya existe un usuario con el mismo DNI, mostrar un mensaje de error
                form.add_error('dni', 'Ya existe un usuario con este DNI.')
                return self.form_invalid(form)
            user = User()
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.dni = form.cleaned_data['dni']
            user.username = user.dni
            # if 'image' in request.FILES:
            #     user.image = request.FILES['image']
            user.create_or_update_password(user.dni)
            user.email = form.cleaned_data['email']
            user.save()
            
            medico = Medico()
            medico.user_id = user.id
            medico.mobile = form.cleaned_data['mobile']
            medico.especialidad = form.cleaned_data['especialidad']
            medico.save()
            group = Group.objects.get(pk=settings.GROUPS.get('medic'))
            user.groups.add(group)
            return HttpResponseRedirect(self.success_url)
        else:
            self.object = None
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return render(request, self.template_name, context)
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un Médico'
        context['action'] = 'add'
        return context


class MedicoUpdateView(PermissionMixin, UpdateView):
    model = Medico
    template_name = 'crm/medico/create.html'  # Reemplaza con el nombre de tu template de actualización
    form_class = MedicoForm
    success_url = reverse_lazy('medico_list')
    permission_required = 'change_medico'
    # object = None

    def get_object(self, queryset=None):
        return super().get_object(queryset=queryset)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        instance = self.get_object()
        form.fields['first_name'].initial = instance.user.first_name
        form.fields['last_name'].initial = instance.user.last_name
        form.fields['dni'].initial = instance.user.dni
        form.fields['email'].initial = instance.user.email
        form.fields['mobile'].initial = instance.mobile
        form.fields['especialidad'].initial = instance.especialidad
        return form

    def form_valid(self, form):
        # Guardar los cambios en el modelo Medico
        medico = form.save(commit=False)
        medico.save()

        # Actualizar los campos del modelo User
        user = medico.user
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.dni = form.cleaned_data['dni']
        user.email = form.cleaned_data['email']
        user.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un Médico'
        context['action'] = 'edit'
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