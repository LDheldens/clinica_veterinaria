from django.urls import reverse_lazy
from django.http import JsonResponse
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, View
from django.http import HttpResponse
import json
from django.db import transaction
from core.pos.models import Cirugia, Client, Medico, Paciente, Diagnostico
from core.pos.forms import CirugiaForm
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
import weasyprint

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
                    cirugia.motivo= request.POST.get('motivo')
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
                cirugia.motivo= request.POST.get('motivo')
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
                    cirugia.motivo= request.POST.get('motivo')
                    cirugia.fecha = request.POST.get('fecha')
                    cirugia.hora = request.POST.get('hora')
                    # Verifica si se proporciona una nueva firma
                    nueva_firma = request.FILES.get('firma_propietario')
                    if nueva_firma:
                        # Si se proporciona una nueva firma, elimina la firma anterior
                        cirugia.firma_propietario.delete(save=False)
                        cirugia.firma_propietario = nueva_firma
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
  

  
#vista para imprimir el acuerdo 
class CirugiaPrintView(View):
    success_url = reverse_lazy('cirugia_list')

    def get(self, request, *args, **kwargs):
        try:
            # Obtén los IDs de los modelos desde la URL
            paciente_id = self.kwargs['paciente_id']
            propietario_id = self.kwargs['propietario_id']
            medico_id = self.kwargs['medico_id']
            
            # Obtén la fecha y la hora de los parámetros de la URL
            fecha = self.kwargs['fecha']
            hora = self.kwargs['hora']
            
            # Convierte la cadena de fecha y hora en objetos datetime si es necesario
            fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
            hora_obj = datetime.strptime(hora, '%H:%M').time()
            
            # Obtén los objetos de los modelos correspondientes
            paciente = get_object_or_404(Paciente, pk=paciente_id)
            propietario = get_object_or_404(Client, pk=propietario_id)
            medico = get_object_or_404(Medico, pk=medico_id)
            
            context = {
                'paciente': paciente,
                'propietario': propietario,
                'medico': medico,
                'fecha': fecha_obj,
                'hora': hora_obj,
            }
            
            template = get_template('crm/cirugia/print/cirugia.html')
            html_template = template.render(context)
            
            # Convierte el HTML a PDF y devuélvelo como respuesta
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'filename="cirugia.pdf"'
            weasyprint.HTML(string=html_template).write_pdf(response)
            return response
        except (Paciente.DoesNotExist, Client.DoesNotExist, Medico.DoesNotExist, Cirugia.DoesNotExist) as e:
            return HttpResponseRedirect(self.get_success_url())