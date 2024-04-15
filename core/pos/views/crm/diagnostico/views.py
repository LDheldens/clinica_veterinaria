import json
from django.utils import timezone
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView
from django.db import transaction
from core.pos.forms import DiagnosticoForm, Diagnostico

class DiagnosticoListView(TemplateView):
    template_name = 'crm/diagnostico/list.html'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = [diagnostico.toJSON() for diagnostico in Diagnostico.objects.all()]
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('diagnostico_create')
        context['title'] = 'Listado de Diagnósticos'
        return context

class DiagnosticoCreateView(CreateView):
    model = Diagnostico
    template_name = 'crm/diagnostico/create.html'
    form_class = DiagnosticoForm
    success_url = reverse_lazy('diagnostico_list')

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action')
        try:
            if action == 'add':
                with transaction.atomic():
                    diagnostico = Diagnostico()
                    diagnostico.paciente_id = request.POST.get('paciente')
                    diagnostico.fecha_diagnostico = request.POST.get('fecha_diagnostico')
                    diagnostico.medico_id = request.POST.get('medico')
                    diagnostico.sintomas = request.POST.get('sintomas')
                    diagnostico.examenes_fisicos = request.POST.get('examenes_fisicos')
                    diagnostico.observacion_veterinario = request.POST.get('observacion_veterinario')
                    diagnostico.diagnostico_provicional = request.POST.get('diagnostico_provicional')
                    diagnostico.save()
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
        context['title'] = 'Nuevo diagnóstico'
        context['action'] = 'add'
        context['instance'] = None
        return context

class DiagnosticoUpdateView(UpdateView):
    model = Diagnostico
    template_name = 'crm/diagnostico/create.html'
    form_class = DiagnosticoForm
    success_url = reverse_lazy('diagnostico_list')

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action')
        try:
            if action == 'edit':
                with transaction.atomic():
                    instance = self.get_object()
                    diagnostico = instance
                    diagnostico.paciente_id = request.POST.get('paciente')
                    fecha_diagnostico_str = request.POST.get('fecha_diagnostico')
                    # Convierte la cadena de fecha a un objeto datetime.date
                    fecha_diagnostico = timezone.datetime.strptime(fecha_diagnostico_str, '%Y-%m-%d').date()
                    diagnostico.fecha_diagnostico = fecha_diagnostico
                    diagnostico.medico_id = request.POST.get('medico')
                    diagnostico.sintomas = request.POST.get('sintomas')
                    diagnostico.examenes_fisicos = request.POST.get('examenes_fisicos')
                    diagnostico.observacion_veterinario = request.POST.get('observacion_veterinario')
                    diagnostico.diagnostico_provicional = request.POST.get('diagnostico_provicional')
                    diagnostico.save()
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = self.success_url
        context['title'] = 'Editar diagnóstico'
        context['action'] = 'edit'
        context['instance'] = self.object
        return context

class DiagnosticoDeleteView(DeleteView):
    model = Diagnostico
    template_name = 'crm/diagnostico/delete.html'
    success_url = reverse_lazy('diagnostico_list')

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
        context['title'] = 'Eliminar diagnóstico'
        context['list_url'] = self.success_url
        return context