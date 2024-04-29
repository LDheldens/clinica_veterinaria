from django.urls import path
from .views.sale_report.views import SaleReportView
from .views.ctascollect_report.views import CtasCollectReportView
from .views.client_report.views import *
from .views.cirugia_report.views import *
from .views.paciente_report.views import *
from .views.hospitalizacion_report.views import *



urlpatterns = [
    path('sale/', SaleReportView.as_view(), name='sale_report'),
    path('ctas/collect/', CtasCollectReportView.as_view(), name='ctascollect_report'),
    path('client/', ClientReportView.as_view(), name='client_report'),
    path('paciente/', PacienteReportView.as_view(), name='paciente_report'),
    path('cirugia/', CirugiaReportView.as_view(), name='cirugia_report'),
    path('hospitalizacion/', HospitalizacionReportView.as_view(), name='hospitalizacion_report'),
]
