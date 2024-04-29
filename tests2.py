from config.wsgi import *
from core.security.models import *
from django.contrib.auth.models import Permission
from core.pos.models import *

dashboard = Dashboard()
dashboard.name = 'Polariss'
dashboard.icon = 'fas fa-shopping-cart'
dashboard.layout = 2
dashboard.card = ' '
dashboard.navbar = 'navbar-dark navbar-primary'
dashboard.brand_logo = ' '
dashboard.sidebar = 'sidebar-light-primary'
dashboard.save()

company = Company()
company.name = 'VETERINARIA'
company.ruc = '000000000000001'
company.email = 'veterianaria@gmail.com'
company.phone = '0000001'
company.mobile = '123456789'
company.desc = 'Salud y cuidado animal'
company.website = 'veterinaria.com'
company.address = 'Jr. Ucayali SN'
company.igv = 18.00
company.save()

type = ModuleType()
type.name = 'Seguridad'
type.icon = 'fas fa-lock'
type.name_menu = 'config'
type.save()
print('insertado {}'.format(type.name))

module = Module()
module.moduletype_id = 1
module.name = 'Tipos de Módulos'
module.url = '/security/module/type/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-door-open'
module.description = 'Permite administrar los tipos de módulos del sistema'
module.save()
for p in Permission.objects.filter(content_type__model=ModuleType._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 1
module.name = 'Módulos'
module.url = '/security/module/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-th-large'
module.description = 'Permite administrar los módulos del sistema'
module.save()
for p in Permission.objects.filter(content_type__model=Module._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 1
module.name = 'Grupos'
module.url = '/security/group/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-users'
module.description = 'Permite administrar los grupos de usuarios del sistema'
module.save()
for p in Permission.objects.filter(content_type__model=Group._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 1
module.name = 'Respaldos'
module.url = '/security/database/backups/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-database'
module.description = 'Permite administrar los respaldos de base de datos'
module.save()
for p in Permission.objects.filter(content_type__model=DatabaseBackups._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 1
module.name = 'Conf. Dashboard'
module.url = '/security/dashboard/update/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-tools'
module.description = 'Permite configurar los datos de la plantilla'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 1
module.name = 'Accesos'
module.url = '/security/access/users/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-user-secret'
module.description = 'Permite administrar los accesos de los usuarios'
module.save()
for p in Permission.objects.filter(content_type__model=AccessUsers._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 1
module.name = 'Usuarios'
module.url = '/user/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-user'
module.description = 'Permite administrar a los administradores del sistema'
module.save()
for p in Permission.objects.filter(content_type__model=User._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

type = ModuleType()
type.name = 'Consultoría'
type.icon = 'fas fa-boxes'
type.name_menu = 'config'
type.save()
print('insertado {}'.format(type.name))

module = Module()
module.moduletype_id = 2
module.name = 'Categorías'
module.url = '/pos/scm/category/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-truck-loading'
module.description = 'Permite administrar las categorías de los productos'
module.save()
for p in Permission.objects.filter(content_type__model=Category._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 2
module.name = 'Servicios'
module.url = '/pos/scm/product/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-box'
module.description = 'Permite administrar los servicios del sistema'
module.save()
for p in Permission.objects.filter(content_type__model=Product._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))


type = ModuleType()
type.name = 'Administrativo'
type.icon = 'fas fa-hand-holding-usd'
type.name_menu = 'config'
type.save()
print('insertado {}'.format(type.name))


module = Module()
module.moduletype_id = 3
module.name = 'Cuentas por cobrar'
module.url = '/pos/frm/ctas/collect/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-funnel-dollar'
module.description = 'Permite administrar las cuentas por cobrar de los clientes'
module.save()
for p in Permission.objects.filter(content_type__model=CtasCollect._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

# Modulo de calendario 
type = ModuleType()
type.name = 'Calendario'
type.icon = 'fas fa-calendar-alt'
type.name_menu = 'clinic'
type.save()
print('insertado {}'.format(type.name))

module = Module()
module.moduletype_id = 4
module.name = 'Calendario'
module.url = '/pos/crm/calendario/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-calendar-alt'
module.description = 'Permite visualisar las citas de a manera de calendario'
module.save()
for p in Permission.objects.filter(content_type__model=Cita._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 4
module.name = 'Registro de citas'
module.url = '/pos/crm/cita/add/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-calendar-plus'
module.description = 'Permite registrar una cita'
module.save()
for p in Permission.objects.filter(content_type__model=Cita._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 4
module.name = 'Listado de citas'
module.url = '/pos/crm/cita/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-list-alt'
module.description = 'Permite listar las citas'
module.save()
for p in Permission.objects.filter(content_type__model=Cita._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

# Modulo de Usuarios
type = ModuleType()
type.name = 'Clientes'
type.icon = 'fas fa-user-friends'
type.name_menu = 'clinic'
type.save()
print('insertado {}'.format(type.name))

module = Module()
module.moduletype_id = 5
module.name = 'Listado de Clientes'
module.url = '/pos/crm/client/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-user-friends'
module.description = 'Permite listar clientes'
module.save()
for p in Permission.objects.filter(content_type__model=Client._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 5
module.name = 'Nuevo Cliente'
module.url = '/pos/crm/client/add/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-user-plus'
module.description = 'Permite agregar un cliente'
module.save()
for p in Permission.objects.filter(content_type__model=Client._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))



type = ModuleType()
type.name = 'Médicos'
type.icon = 'fas fa-user-md'
type.name_menu = 'config'
type.save()
print('insertado {}'.format(type.name))

module = Module()
module.moduletype_id = 6
module.name = 'Listado de médicos'
module.url = '/pos/crm/medico/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-list'
module.description = 'Permite listar los medicos'
module.save()
for p in Permission.objects.filter(content_type__model=Medico._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 6
module.name = 'Nuevo Médico'
module.url = '/pos/crm/medico/add/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-user-plus'
module.description = 'Permite registrar medicos'
module.save()
for p in Permission.objects.filter(content_type__model=Medico._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))



type = ModuleType()
type.name = 'Facturación'
type.icon = 'fas fa-calculator'
type.name_menu = 'config'
type.save()
print('insertado {}'.format(type.name))


module = Module()
module.moduletype_id = 7
module.name = 'Ventas'
module.url = '/pos/crm/sale/admin/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-shopping-cart'
module.description = 'Permite administrar las ventas de los productos'
module.save()
for p in Permission.objects.filter(content_type__model=Sale._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))


type = ModuleType()
type.name = 'Reportes'
type.icon = 'fas fa-chart-pie'
type.name_menu = 'config'
type.save()
print('insertado {}'.format(type.name))

module = Module()
module.moduletype_id = 8
module.name = 'Ventas'
module.url = '/reports/sale/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los reportes de las ventas'
module.save()
print('insertado {}'.format(module.name))


module = Module()
module.moduletype_id = 8
module.name = 'Cuentas por Cobrar'
module.url = '/reports/ctas/collect/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los reportes de las cuentas por cobrar'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 8
module.name = 'Clientes'
module.url = '/reports/client/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los reportes de los clientes'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 8
module.name = 'Pacientes'
module.url = '/reports/paciente/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-file-medical-alt'
module.description = 'Permite ver los reportes de los pacientes'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 8
module.name = 'Cirugias'
module.url = '/reports/cirugia/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-notes-medical'
module.description = 'Permite ver los reportes de las cirugias'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 8
module.name = 'Hospitalización'
module.url = '/reports/hospitalizacion/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-hospital-user'
module.description = 'Permite ver los reportes de las hospitalizaciónes'
module.save()
print('insertado {}'.format(module.name))


type = ModuleType()
type.name = 'Diagnóstico'
type.icon = 'fas fa-stethoscope'
type.name_menu = 'clinic'
type.save()
print('insertado {}'.format(type.name))

module = Module()
module.moduletype_id = 9
module.name = 'Listado de Diagnósticos'
module.url = '/pos/crm/diagnostico/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-file-medical'
module.description = 'Permite listar los diagnosticos'
module.save()
for p in Permission.objects.filter(content_type__model=Diagnostico._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))


module = Module()
module.moduletype_id = 9
module.name = 'Nuevo Diagnóstico'
module.url = '/pos/crm/diagnostico/add/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-diagnoses'
module.description = 'Permite crear un diagnostico'
module.save()
for p in Permission.objects.filter(content_type__model=Diagnostico._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))



type = ModuleType()
type.name = 'Pacientes'
type.icon = 'fas fa-stethoscope'
type.name_menu = 'clinic'
type.save()
print('insertado {}'.format(type.name))

module = Module()
module.moduletype_id = 10
module.name = 'Listado de Pacientes'
module.url = '/pos/crm/paciente/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-list'
module.description = 'Permite listar pacientes'
module.save()
for p in Permission.objects.filter(content_type__model=Paciente._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 10
module.name = 'Nuevo Paciente'
module.url = '/pos/crm/paciente/add/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-paw'
module.description = 'Permite agregar pacientes'
module.save()
for p in Permission.objects.filter(content_type__model=Paciente._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))


type = ModuleType()
type.name = 'Recetas'
type.icon = 'fas fa-book'
type.name_menu = 'clinic'
type.save()
print('insertado {}'.format(type.name))


module = Module()
module.moduletype_id = 11
module.name = 'Listado de Recetas'
module.url = '/pos/crm/receta/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-list'
module.description = 'Permite listar pacientes'
module.save()
for p in Permission.objects.filter(content_type__model=Receta._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

type = ModuleType()
type.name = 'Cirugias'
type.icon = 'fas fa-syringe'
type.name_menu = 'clinic'
type.save()
print('insertado {}'.format(type.name))

module = Module()
module.moduletype_id = 12
module.name = 'Listado de Cirugias'
module.url = '/pos/crm/cirugia/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-notes-medical'
module.description = 'Permite listar las Cirugias'
module.save()
for p in Permission.objects.filter(content_type__model=Cirugia._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 12
module.name = 'Nueva Cirugia'
module.url = '/pos/crm/cirugia/add/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-user-md'
module.description = 'Permite registrar una  Cirugia'
module.save()
for p in Permission.objects.filter(content_type__model=Cirugia._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

type = ModuleType()
type.name = 'Hospitalizaciones'
type.icon = 'fas fa-bed'
type.name_menu = 'clinic'
type.save()
print('insertado {}'.format(type.name))

module = Module()
module.moduletype_id = 13
module.name = 'Listado de Hospitalizaciones'
module.name_menu = 'clinic'
module.url = '/pos/crm/hospitalizacion/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-hospital-user'
module.description = 'Permite listar las hospitalizaciones'
module.save()
for p in Permission.objects.filter(content_type__model=Hospitalizacion._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 13
module.name = 'Nueva Hospitalización'
module.name_menu = 'clinic'
module.url = '/pos/crm/hospitalizacion/add/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-procedures'
module.description = 'Permite agregar una hospitalización'
module.save()
for p in Permission.objects.filter(content_type__model=Hospitalizacion._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))


type = ModuleType()
type.name = 'Baño para Mascotas'
type.icon = 'fas fa-bed'
type.name_menu = 'servi'
type.save()
print('insertado {}'.format(type.name))

module = Module()
module.moduletype_id = 14
module.name = 'Listado de Baños'
module.name_menu = 'servi'
module.url = '/pos/crm/banio/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-hospital-user'
module.description = 'Permite listar las servicios de baños'
module.save()
for p in Permission.objects.filter(content_type__model=Banio._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))

module = Module()
module.moduletype_id = 14
module.name = 'Nueva registro de Baño'
module.name_menu = 'servi'
module.url = '/pos/crm/banio/add/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-procedures'
module.description = 'Permite agregar una registro de Baño'
module.save()
for p in Permission.objects.filter(content_type__model=Banio._meta.label.split('.')[1].lower()):
    module.permits.add(p)
print('insertado {}'.format(module.name))




module = Module()
module.name = 'Tipo de mascotas'
module.url = '/pos/crm/tipo_mascota/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.name_menu = 'config'
module.icon = 'fas fa-paw'
module.description = 'Permite añadir un tipo de mascota'
module.save()
print('insertado {}'.format(module.name))


module = Module()
module.name = 'Historial'
module.name_menu = 'clinic'
module.url = '/pos/crm/historial/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-file-medical'
module.description = 'Permite observar los historiales clínicos'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.name = 'Cambiar password'
module.name_menu = 'config'
module.url = '/user/update/password/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-key'
module.description = 'Permite cambiar tu password de tu cuenta'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.name = 'Editar perfil'
module.name_menu = 'config'
module.url = '/user/update/profile/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-user'
module.description = 'Permite cambiar la información de tu cuenta'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.name = 'Editar perfil'
module.name_menu = 'config'
module.url = '/pos/crm/client/update/profile/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-user'
module.description = 'Permite cambiar la información de tu cuenta'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.name = 'Compañia'
module.name_menu = 'config'
module.url = '/pos/crm/company/update/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-building'
module.description = 'Permite gestionar la información de la compañia'
module.save()
print('insertado {}'.format(module.name))

group = Group()
group.name = 'Administrador'
group.save()
print('insertado {}'.format(group.name))
for m in Module.objects.filter().exclude(url__in=['/pos/crm/client/update/profile/', '/pos/crm/sale/client/']):
    gm = GroupModule()
    gm.module = m
    gm.group = group
    gm.save()
    for perm in m.permits.all():
        group.permissions.add(perm)
        grouppermission = GroupPermission()
        grouppermission.module_id = m.id
        grouppermission.group_id = group.id
        grouppermission.permission_id = perm.id
        grouppermission.save()
        
group = Group()
group.name = 'Medico'
group.save()
print('insertado {}'.format(group.name))
for m in Module.objects.filter().exclude(url__in=['/pos/crm/client/update/profile/', '/pos/crm/sale/client/']):
    gm = GroupModule()
    gm.module = m
    gm.group = group
    gm.save()
    for perm in m.permits.all():
        group.permissions.add(perm)
        grouppermission = GroupPermission()
        grouppermission.module_id = m.id
        grouppermission.group_id = group.id
        grouppermission.permission_id = perm.id
        grouppermission.save()


group = Group()
group.name = 'Cliente'
group.save()
print('insertado {}'.format(group.name))
for m in Module.objects.filter(url__in=['/pos/crm/client/update/profile/', '/pos/crm/sale/client/', '/user/update/password/']).exclude():
    gm = GroupModule()
    gm.module = m
    gm.group = group
    gm.save()

u = User()
u.first_name = 'Cristhian'
u.last_name = 'Chancha Calderon'
u.username = 'admin'
u.dni = '10462002039'
u.email = 'naihtsircnaihtsirc@gmail.com'
u.is_active = True
u.is_superuser = True
u.is_staff = True
u.set_password('Enyaeslamejor12')
u.save()
group = Group.objects.get(pk=1)
u.groups.add(group)
