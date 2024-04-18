from django.urls import path

from core.pos.views.crm.company.views import CompanyUpdateView
from core.pos.views.crm.sale.admin.views import *
from core.pos.views.crm.sale.client.views import SaleClientListView
from core.pos.views.frm.ctascollect.views import *
from core.pos.views.scm.product.views import *
from core.pos.views.scm.category.views import *
from core.pos.views.crm.client.views import *
from core.pos.views.crm.cita.views import *
from core.pos.views.crm.medico.views import *
from core.pos.views.crm.calendario.views import *
from core.pos.views.crm.diagnostico.views import *
from core.pos.views.crm.receta.views import *
from core.pos.views.crm.cirugia.views import *
from core.pos.views.crm.sale.print.views import *


urlpatterns = [
    # company
    path('crm/company/update/', CompanyUpdateView.as_view(), name='company_update'),
    # category
    path('scm/category/', CategoryListView.as_view(), name='category_list'),
    path('scm/category/add/', CategoryCreateView.as_view(), name='category_create'),
    path('scm/category/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('scm/category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
    # product
    path('scm/product/', ProductListView.as_view(), name='product_list'),
    path('scm/product/add/', ProductCreateView.as_view(), name='product_create'),
    path('scm/product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('scm/product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    path('scm/product/export/excel/', ProductExportExcelView.as_view(), name='product_export_excel'),
    # ctascollect
    path('frm/ctas/collect/', CtasCollectListView.as_view(), name='ctascollect_list'),
    path('frm/ctas/collect/add/', CtasCollectCreateView.as_view(), name='ctascollect_create'),
    path('frm/ctas/collect/delete/<int:pk>/', CtasCollectDeleteView.as_view(), name='ctascollect_delete'),
    # client
    path('crm/client/', ClientListView.as_view(), name='client_list'),
    path('crm/client/add/', ClientCreateView.as_view(), name='client_create'),
    path('crm/client/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('crm/client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    path('crm/client/update/profile/', ClientUpdateProfileView.as_view(), name='client_update_profile'),
    # sale/admin
    path('crm/sale/admin/', SaleAdminListView.as_view(), name='sale_admin_list'),
    path('crm/sale/admin/add/', SaleAdminCreateView.as_view(), name='sale_admin_create'),
    path('crm/sale/admin/delete/<int:pk>/', SaleAdminDeleteView.as_view(), name='sale_admin_delete'),
    path('crm/sale/print/voucher/<int:pk>/', SalePrintVoucherView.as_view(), name='sale_print_ticket'),
    path('crm/sale/client/', SaleClientListView.as_view(), name='sale_client_list'),


    # rutas de medicos
    path('crm/medico/', MedicoListView.as_view(), name='medico_list'),
    path('crm/medico/add/', MedicoCreateView.as_view(), name='medico_create'),
    path('crm/medico/update/<int:pk>/', MedicoUpdateView.as_view(), name='medico_update'),
    path('crm/medico/delete/<int:pk>/', MedicoDeleteView.as_view(), name='medico_delete'),

    
    # tipo mascota
    path('crm/tipo_mascota/', TipoMascotaListView.as_view(), name='tipo_mascota_list'),
    path('crm/tipo_mascota/add/', TipoMascotaCreateView.as_view(), name='tipo_mascota_create'),
    path('crm/tipo_mascota/update/<int:pk>/', TipoMascotaUpdateView.as_view(), name='tipo_mascota_update'),
    path('crm/tipo_mascota/delete/<int:pk>/', TipoMascotaDeleteView.as_view(), name='tipo_mascota_delete'),
    
    # Hospitalización
    path('crm/hospitalizacion/', HospitalizacionListView.as_view(), name='hospitalizacion_list'),
    path('crm/hospitalizacion/add/', HospitalizacionCreateView.as_view(), name='hospitalizacion_create'),
    path('crm/hospitalizacion/update/<int:pk>/', HospitalizacionUpdateView.as_view(), name='hospitalizacion_update'),
    path('crm/hospitalizacion/delete/<int:pk>/', HospitalizacionDeleteView.as_view(), name='hospitalizacion_delete'),
    path('crm/hospitalizacion/update_internamiento/<int:pk>/', HospitalizacionUpdateInternamientoView.as_view(), name='hospitalizacion_update_internamiento'),

    # paciente
    path('crm/paciente/', PacienteListView.as_view(), name='paciente_list'),
    path('crm/paciente/add/', PacienteCreateView.as_view(), name='paciente_create'),
    path('crm/paciente/update/<int:pk>/', PacienteUpdateView.as_view(), name='paciente_update'),
    path('crm/paciente/delete/<int:pk>/', PacienteDeleteView.as_view(), name='paciente_delete'),
    
    # citas
    path('crm/cita/', CitaListView.as_view(), name='cita_list'),
    path('crm/cita/cambiar_estado/', CambiarEstadoCitaView.as_view(), name='cambiar_estado_cita'),
    path('crm/cita/add/', CitaCreateView.as_view(), name='cita_create'),
    path('crm/cita/update/<int:pk>/', CitaUpdateView.as_view(), name='cita_update'),
    path('crm/cita/delete/<int:pk>/', CitaDeleteView.as_view(), name='cita_delete'),
    path('crm/cita/cargar_mascotas/', CargarMascotasView.as_view(), name='cargar_mascotas'),
    
    #calendario
    path('crm/calendario/', CalendarioListView.as_view(), name='calendario'),
    path('api/citas/', ListaCitasView.as_view(), name='lista_citas'),
    
    #api para traer todos los medicos, mascotas, clientes
    path('obtener-datos/', ObtenerDatosView.as_view(), name='obtener_datos'),
    
    #citas por envio atraves de js
    path('crm/cita/js/add/', RegistroCitaView.as_view(), name='registro_cita'),
    path('crm/cita/js/edit/<int:cita_id>/', EditarCitaView.as_view(), name='editar_cita'),
    path('crm/cita/js/delete/<int:cita_id>/', EliminarCitaView.as_view(), name='eliminar_cita'),
    
    #diagnostico
    path('crm/diagnostico/', DiagnosticoListView.as_view(), name='diagnostico_list'),
    path('crm/diagnostico/add/', DiagnosticoCreateView.as_view(), name='diagnostico_create'),
    path('crm/diagnostico/update/<int:pk>/', DiagnosticoUpdateView.as_view(), name='diagnostico_update'),
    path('crm/diagnostico/delete/<int:pk>/', DiagnosticoDeleteView.as_view(), name='diagnostico_delete'),
    path('crm/diagnostico/<int:pk>/', DiagnosticoDetailView.as_view(), name='cirugia_detail'),  # Nueva URL para el detalle
    
    #recetas 
    path('crm/receta/', RecetaListView.as_view(), name='receta_list'),
    path('crm/receta/add/', RecetaCreateView.as_view(), name='receta_create'),
    path('crm/receta/update/<int:pk>/', RecetaUpdateView.as_view(), name='receta_update'),
    path('crm/receta/delete/<int:pk>/', RecetaDeleteView.as_view(), name='receta_delete'),
    path('crm/receta/<int:pk>/', RecetaDetailView.as_view(), name='receta_detail'),
    path('crm/receta/print/<int:pk>/', RecetaPrintView.as_view(), name='receta_print'),
    path('crm/ver/receta/', PrevisualizarRecetaView.as_view(),name='xd'),
    
    path('crm/cirugia/', CirugiaListView.as_view(), name='cirugia_list'),
    path('crm/cirugia/add/', CirugiaCreateView.as_view(), name='cirugia_create'),
    path('crm/cirugia/update/<int:pk>/', CirugiaUpdateView.as_view(), name='cirugia_update'),
    path('crm/cirugia/delete/<int:pk>/', CirugiaDeleteView.as_view(), name='cirugia_delete'),

    # path('crm/cirugia/print/<int:paciente_id>/<int:propietario_id>/<int:medico_id>/', CirugiaPrintView.as_view(), name='cirugia_print'),
    path('crm/cirugia/print/<int:paciente_id>/<int:propietario_id>/<int:medico_id>/<fecha>/<hora>/', CirugiaPrintView.as_view(), name='cirugia_print'),
]
