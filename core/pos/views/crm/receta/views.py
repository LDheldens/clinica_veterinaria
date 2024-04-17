from django.http import JsonResponse
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, TemplateView
from django.db import transaction
from django.template.loader import get_template
import weasyprint
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from core.pos.models import Receta, Company
from core.security.mixins import ModuleMixin, PermissionMixin

class RecetaListView(TemplateView):
    template_name = 'crm/receta/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('receta_create')
        context['title'] = 'Listado de Recetas'
        return context

    def post(self, request, *args, **kwargs):
        data = []
        try:
            action = request.POST['action']
            if action == 'search':
                data = [receta.toJSON() for receta in Receta.objects.all()]
            else:
                data['error'] = 'Acción no válida'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

class RecetaCreateView(TemplateView):
    template_name = 'crm/receta/create.html'
    success_url = reverse_lazy('receta_list')
    
    def post(self, request, *args, **kwargs):
        # Lee los datos enviados desde JavaScript
        data = json.loads(request.body)
        
        print(data)

        # Procesa los datos y crea la receta
        if data:
            receta = Receta()
            receta.mascota_id= data['pacienteId']
            receta.medicamentos = data['medicamentos']
            receta.save()
            return JsonResponse({'message': 'Receta creada exitosamente'}, status=201)
        else:
            return JsonResponse({'error': 'No se recibieron datos'}, status=400)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de Receta'
        context['action'] = 'add'
        return context

    
class RecetaUpdateView(UpdateView):
    success_url = reverse_lazy('receta_list')
    
    def post(self, request, *args, **kwargs):
        # Lee los datos enviados desde JavaScript
        data = json.loads(request.body)
        
        # Obtiene la receta que se va a actualizar
        receta = self.get_object()

        # Procesa los datos y actualiza la receta
        if data:
            receta.medicamentos = data['medicamentos']
            receta.save()
            return JsonResponse({'message': 'Receta actualizada exitosamente'})
        else:
            return JsonResponse({'error': 'No se recibieron datos'}, status=400)

    def get_object(self, queryset=None):
        # Obtiene el ID de la receta de los kwargs de la URL
        receta_id = self.kwargs.get('pk')
        # Retorna el objeto Receta correspondiente al ID obtenido
        return Receta.objects.get(pk=receta_id)

class RecetaDeleteView(DeleteView):
    model = Receta
    template_name = 'crm/receta/delete.html'
    success_url = reverse_lazy('receta_list')
    # permission_required = 'delete_receta'

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
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context
    
class RecetaDetailView(View):
    def get(self, request, *args, **kwargs):
        receta_id = kwargs.get('pk')
        
        try:
            receta = Receta.objects.get(id=receta_id)
            medicamentos = receta.medicamentos  # Obtener los medicamentos de la receta
            
            data = {
                'id': receta.id,
                'medicamentos': medicamentos,
                # Agrega otros campos de la receta si los necesitas
            }
            return JsonResponse(data)
        except Receta.DoesNotExist:
            return JsonResponse({'error': 'Receta no encontrada'}, status=404)
        
class RecetaPrintView(View):
    success_url = reverse_lazy('recipe_list')

    def get(self, request, *args, **kwargs):
        try:
            receta = Receta.objects.get(pk=self.kwargs['pk'])
            context = {'receta': receta, 'company': Company.objects.first()}
            template = get_template('crm/receta/print/receta.html')
            html_template = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'filename="receta.pdf"'
            weasyprint.HTML(string=html_template).write_pdf(response)
            return response
        except Receta.DoesNotExist:
            return HttpResponseRedirect(self.get_success_url())
        
        
class PrevisualizarRecetaView(TemplateView):
    template_name = 'crm/receta/print/receta.html'