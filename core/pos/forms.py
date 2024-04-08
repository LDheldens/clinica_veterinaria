from django.forms import ModelForm
from django import forms

from .models import *


class CategoryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ProductForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'category': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'price': forms.TextInput(),
            'pvp': forms.TextInput(),
        }


    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class TipoMascotaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = TipoMascota
        fields = ['tipo_mascota']
        widgets = {
            'tipo_mascota': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese el tipo de mascota',
                    'class': 'form-control',
                    'autocomplete': 'off'
                }
            )
        }

class PacienteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Paciente
        fields = fields = '__all__'
        widgets = {
            'identificacion': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese la identificacion',
                    'class': 'form-control',
                    'autocomplete': 'off'
                }
            ),
            'propietario': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'nombre': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese el propietario',
                    'class': 'form-control',
                    'autocomplete': 'off'
                }
            ),
            'fecha_nacimiento': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'fecha_nacimiento',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#fecha_nacimiento'
            }),
            'tipo_mascota': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'sexo': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'tamanio': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese el tamaño de la mascota',
                    'class': 'form-control',
                    'autocomplete': 'off'
                }
            ),
            'raza': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese la raza',
                    'class': 'form-control',
                    'autocomplete': 'off'
                }
            ),
            'edad': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese la edad',
                    'class': 'form-control',
                    'autocomplete': 'off'
                }
            ),
            'peso': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese el peso',
                    'class': 'form-control',
                    'autocomplete': 'off'
                }
            ),
            'descripcion': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'autocomplete': 'off',
                    'rows': 3,
                    'cols': 3,
                    'placeholder': 'Ingrese una descripción'
                }
            ),
        }

class ClientForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Client
        fields = 'first_name', 'last_name', 'dni', 'email', 'mobile', 'birthdate', 'address'
        widgets = {
            'mobile': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su número celular',
                    'class': 'form-control',
                    'autocomplete': 'off'
                }
            ),
            'address': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese una dirección',
                    'class': 'form-control',
                    'autocomplete': 'off',
                }
            ),
        }
        exclude = ['user']

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off',
        'placeholder': 'Ingrese sus nombres'
    }), label='Nombres', max_length=50)

    birthdate = forms.DateField(input_formats=['%Y-%m-%d'], widget=forms.TextInput(
        attrs={
            'class': 'form-control datetimepicker-input',
            'id': 'birthdate',
            'value': datetime.now().strftime('%Y-%m-%d'),
            'data-toggle': 'datetimepicker',
            'data-target': '#birthdate'
        }), label='Fecha de nacimiento')

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off',
        'placeholder': 'Ingrese sus apellidos'
    }), label='Apellidos', max_length=50)

    dni = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off',
        'placeholder': 'Ingrese su número de cedula'
    }), label='Número de cedula', max_length=10)

    email = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off',
        'placeholder': 'Ingrese su email'
    }), label='Email', max_length=50)

    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }), label='Imagen')


class SaleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].queryset = Client.objects.none()

    class Meta:
        model = Sale
        fields = '__all__'
        widgets = {
            'client': forms.Select(attrs={'class': 'custom-select select2'}),
            'payment_condition': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'payment_method': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'type_voucher': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'date_joined': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'date_joined',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#date_joined'
            }),
            'end_credit': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'end_credit',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#end_credit'
            }),
            'subtotal': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'disabled': True
            }),
            'igv': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'disabled': True
            }),
            'total_igv': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'disabled': True
            }),
            'dscto': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'autocomplete': 'off'
            }),
            'total_dscto': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'disabled': True
            }),
            'total': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'disabled': True
            }),
            'cash': forms.TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off'
            }),
            'change': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': True
            }),
            'card_number': forms.TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'placeholder': 'Ingrese el número de la tarjeta'
            }),
            'titular': forms.TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'placeholder': 'Ingrese el nombre del titular'
            }),
            'amount_debited': forms.TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'readonly': True
            }),
        }

    amount = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off',
        'disabled': True
    }))


class PaymentsCtaCollectForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['valor'].widget.attrs['autofocus'] = True
        self.fields['ctascollect'].queryset = PaymentsCtaCollect.objects.none()

    class Meta:
        model = PaymentsCtaCollect
        fields = '__all__'
        widgets = {
            'ctascollect': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'date_joined': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'date_joined',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#date_joined'
            }),
            'valor': forms.TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
            }),
            'desc': forms.Textarea(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'rows': 3,
                'cols': 3,
                'placeholder': 'Ingrese una descripción'
            }),
        }


class CompanyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True
        for form in self.visible_fields():
            form.field.widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = Company
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'ruc': forms.TextInput(attrs={'placeholder': 'Ingrese un ruc'}),
            'mobile': forms.TextInput(attrs={'placeholder': 'Ingrese un teléfono celular'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Ingrese un teléfono convencional'}),
            'email': forms.TextInput(attrs={'placeholder': 'Ingrese un email'}),
            'address': forms.TextInput(attrs={'placeholder': 'Ingrese una dirección'}),
            'website': forms.TextInput(attrs={'placeholder': 'Ingrese una dirección web'}),
            'desc': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': 3}),
            'igv': forms.TextInput(),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class CitaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CitaForm, self).__init__(*args, **kwargs)
        
        # Cargar opciones para el campo de selección de médico
        medicos = Medico.objects.all()
        self.fields['medico'].queryset = medicos
        
        # Cargar opciones para el campo de selección de propietario
        propietarios = Client.objects.all()
        self.fields['propietario'].queryset = propietarios
        
        # Cargar opciones para el campo de selección de mascota
        mascotas = Paciente.objects.all()
        self.fields['mascota'].queryset = mascotas

    class Meta:
        model = Cita
        fields = ['medico', 'asunto', 'descripcion', 'fecha_cita', 'hora_cita', 'propietario', 'mascota']
        labels = {
            'medico': 'Médico',
            'asunto': 'Asunto',
            'descripcion': 'Descripción',
            'fecha_cita': 'Fecha de la cita',
            'hora_cita': 'Hora de la cita',
            'propietario': 'Propietario',
            'mascota': 'Mascota',
        }
        widgets = {
            'fecha_cita': forms.DateInput(format='%Y-%m-%d',attrs={'type': 'date', 'class': 'form-control'}),
            'hora_cita': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'medico': forms.Select(attrs={'class': 'form-control'}),
            'asunto': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'propietario': forms.Select(attrs={'class': 'form-control'}),
            'mascota': forms.Select(attrs={'class': 'form-control'}),
        }
        
class MedicoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Medico
        fields = ['especialidad', 'first_name', 'last_name', 'dni', 'email', 'mobile']
        widgets = {
            'especialidad': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese la especialidad',
                    'class': 'form-control',
                    'autocomplete': 'off'
                }
            ),
            'mobile': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su número celular',
                    'class': 'form-control',
                    'autocomplete': 'off',
                    'max_length':9
                }
            ),
        }

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off',
        'placeholder': 'Ingrese sus nombres'
    }), label='Nombres', max_length=50)

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off',
        'placeholder': 'Ingrese sus apellidos'
    }), label='Apellidos', max_length=50)

    dni = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off',
        'placeholder': 'Ingrese su número de cedula'
    }), label='Número de DNI', max_length=8)

    email = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off',
        'placeholder': 'Ingrese su email'
    }), label='Email', max_length=50)

    # image = forms.ImageField(widget=forms.FileInput(attrs={
    #     'class': 'form-control',
    #     'autocomplete': 'off'
    # }), label='Imagen')