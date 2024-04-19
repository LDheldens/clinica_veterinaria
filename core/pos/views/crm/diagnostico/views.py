import json
from django.shortcuts import get_object_or_404
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView, View
from django.db import transaction
from core.pos.forms import DiagnosticoForm, Diagnostico

class DiagnosticoListView(TemplateView):
    template_name = 'crm/diagnostico/list.html'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action')
            if action == 'search':
                # Obtener todos los diagnósticos ordenados por fecha de diagnóstico de más recientes a más antiguas
                diagnosticos = Diagnostico.objects.all().order_by('-fecha_diagnostico')
                # Convertir los diagnósticos a formato JSON utilizando DjangoJSONEncoder
                data = [diagnostico.toJSON() for diagnostico in diagnosticos]
                return JsonResponse(data, encoder=DjangoJSONEncoder, safe=False)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

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
                    diagnostico.temperatura = float(request.POST.get('temperatura', 0))  # Convertir a float
                    diagnostico.mucosa = request.POST.get('mucosa')
                    diagnostico.motivo_consulta = request.POST.get('motivo_consulta')
                    diagnostico.sintomas = request.POST.get('sintomas')
                    diagnostico.examenes_realizados = request.POST.get('examenes_realizados')
                    diagnostico.observaciones_veterinario = request.POST.get('observaciones_veterinario')
                    diagnostico.diagnostico_provicional = request.POST.get('diagnostico_provicional')
                    diagnostico.condicion_llegada = request.POST.get('condicion_llegada')
                    diagnostico.frecuencia_cardiaca = request.POST.get('frecuencia_cardiaca', 0)
                    diagnostico.frecuencia_respiratoria = request.POST.get('frecuencia_respiratoria', 0)
                    diagnostico.esterilizado = True if request.POST.get('esterilizado') == 'on' else False
                    diagnostico.save()
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

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
        print('PROBANDO', request.POST)
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
                    diagnostico.medico_id = request.POST.get('medico')
                    diagnostico.temperatura = float(request.POST.get('temperatura', 0))
                    diagnostico.fecha_diagnostico = fecha_diagnostico
                    diagnostico.mucosa = request.POST.get('mucosa')
                    diagnostico.motivo_consulta = request.POST.get('motivo_consulta')
                    diagnostico.sintomas = request.POST.get('sintomas')
                    diagnostico.examenes_realizados = request.POST.get('examenes_realizados')
                    diagnostico.observaciones_veterinario = request.POST.get('observaciones_veterinario')
                    diagnostico.diagnostico_provicional = request.POST.get('diagnostico_provicional')
                    diagnostico.condicion_llegada = request.POST.get('condicion_llegada')
                    diagnostico.frecuencia_cardiaca = request.POST.get('frecuencia_cardiaca', 0)
                    diagnostico.frecuencia_respiratoria = request.POST.get('frecuencia_respiratoria', 0)
                    diagnostico.esterilizado = True if request.POST.get('esterilizado') == 'on' else False
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
    
class DiagnosticoDetailView(View):
    model = Diagnostico

    def get(self, request, *args, **kwargs):
        print('PROBANDO: FTGHGF')
        # Obtener el id de la URL
        diagnostico_id = kwargs.get('pk')

        # Obtener la instancia de Diagnostico o devolver un error 404 si no se encuentra
        diagnostico = get_object_or_404(Diagnostico, pk=diagnostico_id)

        # Crear el diccionario de datos para la respuesta JSON
        data = {
            'id': diagnostico.id,
            'motivo': diagnostico.diagnostico_provicional
        }

        # Devolver la respuesta JSON
        return JsonResponse(data)