import json

from django.http import HttpResponse
from django.views.generic import FormView

from core.pos.models import Sale, Client
from core.reports.forms import ReportForm
from core.security.mixins import ModuleMixin


class ClientReportView(FormView):
    template_name = 'client_report/report.html'
    form_class = ReportForm

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
        context['title'] = 'Reporte de Clientes'
        return context
