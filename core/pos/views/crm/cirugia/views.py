from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse
import json
from django.db import transaction
from core.pos.models import Cirugia
from core.pos.forms import CirugiaForm

class CirugiaListView(TemplateView):
    template_name = 'crm/cirugia/list.html'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action')
            if action == 'search':
                cirugias = Cirugia.objects.all().order_by('-fecha')
                data = [cirugia.toJSON() for cirugia in cirugias]
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('cirugia_create')
        context['title'] = 'Listado de Cirugías'
        return context

class CirugiaCreateView(CreateView):
    model = Cirugia
    template_name = 'crm/cirugia/create.html'
    form_class = CirugiaForm
    success_url = reverse_lazy('cirugia_list')

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action')
        try:
            if action == 'add':
                with transaction.atomic():
                    cirugia = Cirugia()
                    cirugia.paciente_id =  request.POST.get('paciente')
                    cirugia.medico_id = request.POST.get('medico')
                    cirugia.cliente_id = request.POST.get('cliente')
                    cirugia.fecha = request.POST.get('fecha')
                    cirugia.hora = request.POST.get('hora')
                    cirugia.firma_propietario = request.FILES.get('firma_propietario')
                    cirugia.save()
            elif action == 'add2':
                print('PROBANDO:', request.POST)
                cirugia = Cirugia()
                cirugia.paciente_id =  request.POST.get('paciente')
                cirugia.medico_id = request.POST.get('medico')
                cirugia.cliente_id = request.POST.get('cliente')
                cirugia.fecha = request.POST.get('fecha')
                cirugia.hora = request.POST.get('hora')
                cirugia.firma_propietario = request.FILES.get('firma_propietario')
                cirugia.save()
                
                print('SE CREÓ LA CIRUGIA')
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nueva Cirugía'
        context['action'] = 'add'
        context['instance'] = None
        return context

class CirugiaUpdateView(UpdateView):
    model = Cirugia
    template_name = 'crm/cirugia/create.html'
    form_class = CirugiaForm
    success_url = reverse_lazy('cirugia_list')

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action')
        try:
            if action == 'edit':
                with transaction.atomic():
                    cirugia = self.get_object()
                    cirugia.paciente_id =  request.POST.get('paciente')
                    cirugia.medico_id = request.POST.get('medico')
                    cirugia.cliente_id = request.POST.get('cliente')
                    cirugia.fecha = request.POST.get('fecha')
                    cirugia.hora = request.POST.get('hora')
                    cirugia.firma_propietario = request.POST.get('firma_propietario')
                    cirugia.save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = self.success_url
        context['title'] = 'Editar Cirugía'
        context['action'] = 'edit'
        return context

class CirugiaDeleteView(DeleteView):
    model = Cirugia
    template_name = 'crm/cirugia/delete.html'
    success_url = reverse_lazy('cirugia_list')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            with transaction.atomic():
                self.get_object().delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Cirugía'
        context['list_url'] = self.success_url
        return context