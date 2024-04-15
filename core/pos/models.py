import math
import os
import re
from datetime import datetime
from datetime import date
from django.utils import timezone
from django.db import models
from django.db.models import FloatField
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.forms import model_to_dict
from django.core.exceptions import ValidationError
from config import settings
from core.pos.choices import payment_condition, payment_method, voucher, sexo_mascota, unidad_edad
from core.user.models import User


class Company(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre')
    ruc = models.CharField(max_length=13, verbose_name='Ruc')
    address = models.CharField(max_length=200, verbose_name='Dirección')
    mobile = models.CharField(max_length=10, verbose_name='Teléfono celular')
    phone = models.CharField(max_length=9, verbose_name='Teléfono convencional')
    email = models.CharField(max_length=50, verbose_name='Email')
    website = models.CharField(max_length=250, verbose_name='Página web')
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')
    image = models.ImageField(null=True, blank=True, upload_to='company/%Y/%m/%d', verbose_name='Logo')
    igv = models.DecimalField(default=0.00, decimal_places=2, max_digits=9, verbose_name='Igv')

    def __str__(self):
        return self.name

    def get_image(self):
        if self.image:
            return '{}{}'.format(settings.MEDIA_URL, self.image)
        return '{}{}'.format(settings.STATIC_URL, 'img/default/empty.png')

    def get_igv(self):
        return format(self.igv, '.2f')

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        default_permissions = ()
        permissions = (
            ('view_company', 'Can view Company'),
        )
        ordering = ['-id']


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Nombre')
    inventoried = models.BooleanField(default=True, verbose_name='¿Es inventariado?')

    def __str__(self):
        return '{} / {}'.format(self.name, self.get_inventoried())

    def get_inventoried(self):
        if self.inventoried:
            return 'Inventariado'
        return 'No inventariado'

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['-id']

class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Categoría')
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Precio de Compra')
    pvp = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Precio de Venta')
    image = models.ImageField(upload_to='product/%Y/%m/%d', verbose_name='Imagen', null=True, blank=True)

    def __str__(self):
        return self.name

    def remove_image(self):
        try:
            if self.image:
                os.remove(self.image.path)
        except:
            pass
        finally:
            self.image = None

    def toJSON(self):
        item = model_to_dict(self)
        item['category'] = self.category.toJSON()
        item['price'] = format(self.price, '.2f')
        item['price_promotion'] = format(self.get_price_promotion(), '.2f')
        item['price_current'] = format(self.get_price_current(), '.2f')
        item['pvp'] = format(self.pvp, '.2f')
        item['image'] = self.get_image()
        return item

    def get_price_promotion(self):
        promotions = self.promotionsdetail_set.filter(promotion__state=True)
        if promotions.exists():
            return promotions[0].price_final
        return 0.00

    def get_price_current(self):
        price_promotion = self.get_price_promotion()
        if price_promotion > 0:
            return price_promotion
        return self.pvp

    def get_image(self):
        if self.image:
            return '{}{}'.format(settings.MEDIA_URL, self.image)
        return '{}{}'.format(settings.STATIC_URL, 'img/default/empty.png')

    def delete(self, using=None, keep_parents=False):
        try:
            os.remove(self.image.path)
        except:
            pass
        super(Product, self).delete()

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-name']


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=10, unique=True, verbose_name='Teléfono')
    birthdate = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    address = models.CharField(max_length=500, null=True, blank=True, verbose_name='Dirección')

    def __str__(self):
        return '{} / {}'.format(self.user.get_full_name(), self.user.dni)

    def birthdate_format(self):
        return self.birthdate.strftime('%Y-%m-%d')

    def toJSON(self):
        item = model_to_dict(self)
        item['user'] = self.user.toJSON()
        item['birthdate'] = self.birthdate.strftime('%Y-%m-%d')
        return item

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['-id']



class Sale(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT, null=True, blank=True)
    employee = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    payment_condition = models.CharField(choices=payment_condition, max_length=50, default='contado')
    payment_method = models.CharField(choices=payment_method, max_length=50, default='efectivo')
    type_voucher = models.CharField(choices=voucher, max_length=50, default='ticket')
    date_joined = models.DateField(default=datetime.now)
    end_credit = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    dscto = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    total_dscto = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    igv = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    total_igv = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    cash = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    change = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    card_number = models.CharField(max_length=30, null=True, blank=True)
    titular = models.CharField(max_length=30, null=True, blank=True)
    amount_debited = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.client.user.get_full_name()} / {self.nro()}'

    def nro(self):
        return format(self.id, '06d')

    def get_client(self):
        if self.client:
            return self.client.toJSON()
        return {}

    def card_number_format(self):
        if self.card_number:
            cardnumber = self.card_number.split(' ')
            convert = re.sub('[0-9]', 'X', ' '.join(cardnumber[1:]))
            return '{} {}'.format(cardnumber[0], convert)
        return self.card_number

    def toJSON(self):
        item = model_to_dict(self, exclude=[''])
        item['nro'] = format(self.id, '06d')
        item['card_number'] = self.card_number_format()
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['end_credit'] = self.end_credit.strftime('%Y-%m-%d')
        item['employee'] = {} if self.employee is None else self.employee.toJSON()
        item['client'] = {} if self.client is None else self.client.toJSON()
        item['payment_condition'] = {'id': self.payment_condition, 'name': self.get_payment_condition_display()}
        item['payment_method'] = {'id': self.payment_method, 'name': self.get_payment_method_display()}
        item['type_voucher'] = {'id': self.type_voucher, 'name': self.get_type_voucher_display()}
        item['subtotal'] = format(self.subtotal, '.2f')
        item['dscto'] = format(self.dscto, '.2f')
        item['total_dscto'] = format(self.total_dscto, '.2f')
        item['igv'] = format(self.igv, '.2f')
        item['total_igv'] = format(self.total_igv, '.2f')
        item['total'] = format(self.total, '.2f')
        item['cash'] = format(self.cash, '.2f')
        item['change'] = format(self.change, '.2f')
        item['amount_debited'] = format(self.amount_debited, '.2f')
        return item

    def calculate_invoice(self):
        subtotal = 0.00
        for d in self.saledetail_set.filter():
            d.subtotal = float(d.price) * int(d.cant)
            d.total_dscto = float(d.dscto) * float(d.subtotal)
            d.total = d.subtotal - d.total_dscto
            d.save()
            subtotal += d.total
        self.subtotal = subtotal
        self.total_igv = self.subtotal * float(self.igv)
        self.total_dscto = self.subtotal * float(self.dscto)
        self.total = float(self.subtotal) - float(self.total_dscto) + float(self.total_igv)
        self.save()

    def delete(self, using=None, keep_parents=False):
        try:
            for i in self.saledetail_set.filter(product__category__inventoried=True):
                i.product.save()
                i.delete()
        except:
            pass
        super(Sale, self).delete()

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        default_permissions = ()
        permissions = (
            ('view_sale', 'Can view Ventas'),
            ('add_sale', 'Can add Ventas'),
            ('delete_sale', 'Can delete Ventas'),
        )
        ordering = ['-id']


class SaleDetail(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    cant = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    dscto = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    total_dscto = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return self.product.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['product'] = self.product.toJSON()
        item['price'] = format(self.price, '.2f')
        item['dscto'] = format(self.dscto, '.2f')
        item['total_dscto'] = format(self.total_dscto, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        item['total'] = format(self.total, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'
        default_permissions = ()
        ordering = ['-id']


class CtasCollect(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.PROTECT)
    date_joined = models.DateField(default=datetime.now)
    end_date = models.DateField(default=datetime.now)
    debt = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    saldo = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    state = models.BooleanField(default=True)

    def __str__(self):
        return '{} / {} / ${}'.format(self.sale.client.user.get_full_name(), self.date_joined.strftime('%Y-%m-%d'),
                                      format(self.debt, '.2f'))

    def validate_debt(self):
        try:
            saldo = self.paymentsctacollect_set.aggregate(resp=Coalesce(Sum('valor'), 0.00, output_field=FloatField())).get('resp')
            self.saldo = float(self.debt) - float(saldo)
            self.state = self.saldo > 0.00
            self.save()
        except:
            pass

    def toJSON(self):
        item = model_to_dict(self)
        item['sale'] = self.sale.toJSON()
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['end_date'] = self.end_date.strftime('%Y-%m-%d')
        item['debt'] = format(self.debt, '.2f')
        item['saldo'] = format(self.saldo, '.2f')
        return item

    class Meta:
        verbose_name = 'Cuenta por cobrar'
        verbose_name_plural = 'Cuentas por cobrar'
        default_permissions = ()
        permissions = (
            ('view_ctascollect', 'Can view Cuentas por cobrar'),
            ('add_ctascollect', 'Can add Cuentas por cobrar'),
            ('delete_ctascollect', 'Can delete Cuentas por cobrar'),
        )
        ordering = ['-id']


class PaymentsCtaCollect(models.Model):
    ctascollect = models.ForeignKey(CtasCollect, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de registro')
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Detalles')
    valor = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Valor')

    def __str__(self):
        return self.ctascollect.id

    def toJSON(self):
        item = model_to_dict(self, exclude=['ctascollect'])
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['valor'] = format(self.valor, '.2f')
        return item

    class Meta:
        verbose_name = 'Pago Cuenta por cobrar'
        verbose_name_plural = 'Pagos Cuentas por cobrar'
        default_permissions = ()
        ordering = ['-id']


# MODELOS 
class Medico(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    especialidad = models.CharField(max_length = 150)
    mobile = models.CharField(max_length=9, unique=True, verbose_name='Teléfono')
    codigo_medico = models.CharField(max_length=10, verbose_name='Código del medico veterinario', blank=True, null=True)
    
    def __str__(self):
        return '{} / {}'.format(self.user.get_full_name(), self.user.dni)
    
    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = self.user.get_full_name()
        item['imagen'] = self.user.get_image()
        item['dni'] = self.user.dni
        return item

class TipoMascota(models.Model):
    tipo_mascota = models.CharField(max_length = 150)
    def toJSON(self):
        item = model_to_dict(self)
        return item
    def __str__(self):
        return f'{self.tipo_mascota}'   
  
class Paciente(models.Model):
    identificacion = models.CharField(max_length=150, verbose_name='Identificación de la mascota')
    propietario = models.ForeignKey(Client, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150, verbose_name='Nombre de la mascota')
    fecha_nacimiento = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')  
    tipo_mascota = models.ForeignKey(TipoMascota, on_delete=models.CASCADE)
    sexo = models.CharField(choices=sexo_mascota, max_length=150, default="sin especificar")
    tamanio = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Tamaño') 
    raza = models.CharField(max_length=150, null=True, blank=True)
    unidad_edad = models.CharField(max_length=20, choices=unidad_edad, default="año(s)", verbose_name='Unidad de edad')
    edad = models.IntegerField()
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    descripcion = models.TextField(null=True, blank=True, verbose_name='Caracteristicas del paciente')
    
    def __str__(self):
        return f'{self.nombre} / {self.tipo_mascota} / {self.raza}'    
    
    def toJSON(self):
        item = model_to_dict(self)
        print(item)
        item['tipo_mascota'] = self.tipo_mascota.toJSON()['tipo_mascota']
        item['propietario'] = self.propietario.toJSON()['user']['full_name']
        item['fecha_nacimiento'] = self.fecha_nacimiento.strftime('%Y-%m-%d')
        item['tamanio'] = format(self.tamanio, '.2f')
        item['peso'] = format(self.peso, '.2f')
        return item

class Diagnostico(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='diagnosticos')
    fecha_diagnostico = models.DateField(default=date.today, verbose_name='Fecha del diagnóstico')
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, verbose_name='Médico veterinario')
    sintomas = models.CharField(max_length=100, verbose_name='Sintomas del paciente')
    examenes_fisicos = models.TextField(verbose_name='Exámenes realizados')
    observacion_veterinario = models.TextField(max_length=300, verbose_name='Observación del Veterinario')
    diagnostico_provicional = models.TextField(max_length=300, verbose_name='Diagnóstico Provicional')

    def __str__(self):
        return f'Diagnóstico para {self.paciente} - {self.fecha_diagnostico.strftime("%Y-%m-%d")}'
    
    def toJSON(self):
        item = model_to_dict(self)
        item['paciente'] = self.paciente.toJSON()
        item['medico'] = self.medico.toJSON()
        item['fecha_diagnostico'] = self.fecha_diagnostico.strftime('%Y-%m-%d')
        return item

class Cita(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    asunto = models.TextField(verbose_name='Asunto')
    descripcion = models.TextField(verbose_name='Descripción', null=True)
    fecha_cita = models.DateField(auto_now=False, auto_now_add=False, verbose_name='Fecha de la cita')
    hora_cita = models.TimeField(auto_now=False, auto_now_add=False, verbose_name='Hora de la cita')
    propietario = models.ForeignKey(Client, on_delete=models.CASCADE)
    mascota = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    estado = models.BooleanField( default=False)

    def toJSON(self):
        item = {
            'id': self.id,
            'asunto': self.asunto,
            'descripcion': self.descripcion,
            'fecha_cita': self.fecha_cita.strftime('%Y-%m-%d'),
            'hora_cita': self.hora_cita.strftime('%H:%M:%S'),
            'estado': self.estado,
            'medico': {
                'id': self.medico.id,
                'nombre': self.medico.user.first_name if self.medico else None,
                'apellidos': self.medico.user.last_name if self.medico else None,
            },
            'propietario': {
                'id': self.propietario.id,  # Agregar el ID del propietario
                'nombre': self.propietario.user.first_name if self.propietario else None,
                'apellidos': self.propietario.user.last_name if self.propietario else None,
            },
            'mascota': {
                'id': self.mascota.id,  # Agregar el ID de la mascota
                'nombre': self.mascota.nombre if self.mascota else None,
                'mascota_full_data': f'{self.mascota.nombre} / {self.mascota.tipo_mascota} / {self.mascota.raza}' if self.mascota else None,
            },
        }
        return item

class Hospitalizacion(models.Model):
    mascota = models.ForeignKey(Paciente, on_delete=models.CASCADE, verbose_name='Mascota')
    fecha_ingreso = models.DateField(default=datetime.now, verbose_name='Fecha de ingreso')
    fecha_salida = models.DateField(default=datetime.now, verbose_name='Fecha de salida')
    medicinas_aplicadas = models.CharField(max_length=400, verbose_name='Medicinas aplicadas')
    motivo = models.CharField(max_length=150, verbose_name='Motivo')
    antecedentes = models.TextField(verbose_name='Antecedentes')
    tratamiento = models.CharField(max_length=200, verbose_name='Tratamiento')
    internado = models.BooleanField(default=True, verbose_name='Internado')

    def dias_internados(self):
        now = datetime.now().date() 
        result = now - self.fecha_ingreso
        return result.days

    def toJSON(self):
        item = model_to_dict(self)
        item['fecha_ingreso'] = self.fecha_ingreso.strftime('%Y-%m-%d')
        item['fecha_salida'] = self.fecha_salida.strftime('%Y-%m-%d')
        item['dias_internados'] = self.dias_internados()
        # item['estado'] = 'internado' if self.internado else 'dado de alta',
        return item