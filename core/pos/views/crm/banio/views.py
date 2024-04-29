from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, View
from django.db import transaction
import json
from core.pos.models import Banio, Client, Paciente
from core.pos.forms import BanioForm
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
import weasyprint

class BanioListView(TemplateView):
    template_name = 'crm/banio/list.html'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action')
            if action == 'search':
                banios = Banio.objects.all().order_by('-hora_ingreso')
                data = [banio.toJSON() for banio in banios]
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('banio_create')
        context['title'] = 'Listado de Baños'
        return context

class BanioCreateView(CreateView):
    model = Banio
    template_name = 'crm/banio/create.html'
    form_class = BanioForm
    success_url = reverse_lazy('banio_list')

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action')
        try:
            if action == 'add':
                with transaction.atomic():
                    banio = Banio()
                    banio.cliente_id = request.POST.get('cliente')
                    banio.paciente_id = request.POST.get('paciente')
                    banio.detalles_banio = request.POST.get('detalles_banio')
                    banio.hora_ingreso = request.POST.get('hora_ingreso')
                    banio.hora_salida = request.POST.get('hora_salida')
                    banio.save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo Baño'
        context['action'] = 'add'
        context['instance'] = None
        return context

class BanioUpdateView(UpdateView):
    model = Banio
    template_name = 'crm/banio/create.html'
    form_class = BanioForm
    success_url = reverse_lazy('banio_list')

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action')
        try:
            if action == 'edit':
                with transaction.atomic():
                    banio = self.get_object()
                    banio.cliente_id = request.POST.get('cliente')
                    banio.paciente_id = request.POST.get('paciente')
                    banio.detalles_banio = request.POST.get('detalles_banio')
                    banio.hora_ingreso = request.POST.get('hora_ingreso')
                    banio.hora_salida = request.POST.get('hora_salida')
                    banio.save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = self.success_url
        context['title'] = 'Editar Baño'
        context['action'] = 'edit'
        return context

class BanioDeleteView(DeleteView):
    model = Banio
    template_name = 'crm/banio/delete.html'
    success_url = reverse_lazy('banio_list')

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
        context['title'] = 'Eliminar Baño'
        context['list_url'] = self.success_url
        return context
