import json
import weasyprint
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.models import Group
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View
from django.core.serializers.json import DjangoJSONEncoder
from config import settings
from core.pos.forms import HistorialClinico, Paciente
from core.security.mixins import ModuleMixin, PermissionMixin
from django.core.serializers.json import DjangoJSONEncoder



class HistoriaListView(PermissionMixin, TemplateView):
    template_name = 'crm/historial/list.html'
    permission_required = 'view_paciente'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                historiales = HistorialClinico.objects.all()
                data = [historial.toJSON() for historial in historiales]
                return JsonResponse(data, encoder=DjangoJSONEncoder, safe=False)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        # Serializar los datos a JSON
        return JsonResponse(data, encoder=DjangoJSONEncoder)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('paciente_create')
        context['title'] = 'Listado de Historiales clínicos'
        return context

class HistorialPrintView(View):
    success_url = reverse_lazy('historial_list')

    def get(self, request, *args, **kwargs):
        try:
            paciente_id = self.kwargs['paciente_id']
            # Obtener el objeto del modelo Paciente con el ID proporcionado
            paciente = get_object_or_404(Paciente, pk=paciente_id)

            # Obtener todos los registros relacionados con el paciente
            diagnosticos = paciente.get_diagnosticos()
            citas = paciente.get_citas()
            hospitalizaciones = paciente.get_hospitalizaciones()
            recetas = paciente.get_recetas()
            cirugias = paciente.get_cirugias()
            historial_clinico = paciente.get_historial_clinico()

            context = {
                'paciente': paciente,
                'diagnosticos': diagnosticos,
                'citas': citas,
                'hospitalizaciones': hospitalizaciones,
                'recetas': recetas,
                'cirugias': cirugias,
                'historial_clinico': historial_clinico,
            }
            
            template = get_template('crm/historial/print/historial.html')
            html_template = template.render(context)
            
            # Convertir el HTML a PDF y devolverlo como respuesta
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'filename="historial.pdf"'
            weasyprint.HTML(string=html_template).write_pdf(response)
            return response
        except Paciente.DoesNotExist:
            return HttpResponseRedirect(self.success_url)