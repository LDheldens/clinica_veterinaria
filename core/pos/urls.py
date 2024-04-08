from django.urls import path

from core.pos.views.crm.company.views import CompanyUpdateView
from core.pos.views.crm.sale.admin.views import *
from core.pos.views.crm.sale.client.views import SaleClientListView
from core.pos.views.frm.ctascollect.views import *
from core.pos.views.scm.product.views import *
from core.pos.views.scm.category.views import *
from core.pos.views.crm.client.views import *
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
    path('crm/medico/', ClientListView.as_view(), name='medico_list'),
    path('crm/medico/add/', ClientCreateView.as_view(), name='medico_create'),
    path('crm/medico/update/<int:pk>/', ClientUpdateView.as_view(), name='medico_update'),
    path('crm/medico/delete/<int:pk>/', ClientDeleteView.as_view(), name='medico_delete'),
    
    # tipo mascota
    path('crm/tipo_mascota/', TipoMascotaListView.as_view(), name='tipo_mascota_list'),
    path('crm/tipo_mascota/add/', TipoMascotaCreateView.as_view(), name='tipo_mascota_create'),
    path('crm/tipo_mascota/update/<int:pk>/', TipoMascotaUpdateView.as_view(), name='tipo_mascota_update'),
    path('crm/tipo_mascota/delete/<int:pk>/', TipoMascotaDeleteView.as_view(), name='tipo_mascota_delete'),
    
    # paciente
    path('crm/paciente/', PacienteListView.as_view(), name='paciente_list'),
    path('crm/paciente/add/', PacienteCreateView.as_view(), name='paciente_create'),
    path('crm/paciente/update/<int:pk>/', PacienteUpdateView.as_view(), name='paciente_update'),
    path('crm/paciente/delete/<int:pk>/', PacienteDeleteView.as_view(), name='paciente_delete'),
    
    # citas
    path('crm/cita/', ClientListView.as_view(), name='cita_list'),
    path('crm/calendario/', ClientListView.as_view(), name='cita_list'),
    path('crm/cita/add/', ClientCreateView.as_view(), name='cita_create'),
    path('crm/cita/update/<int:pk>/', ClientUpdateView.as_view(), name='cita_update'),
    path('crm/cita/delete/<int:pk>/', ClientDeleteView.as_view(), name='cita_delete'),
]
