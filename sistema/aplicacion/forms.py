from django import forms
from .models import *

class CustomClearableFileInput(forms.ClearableFileInput):
    initial_text = 'Imagen anterior'        # reemplaza “Currently”
    input_text = 'Subir nueva imagen'       # reemplaza “Change”
    template_name = 'django/forms/widgets/clearable_file_input.html'

class ProductoForm(forms.ModelForm):
    class Meta:
        model = productos
        fields = '__all__'
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripcion'}),
            'marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Marca'}),
            'procedencia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Procedencia'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stockmaximo': forms.NumberInput(attrs={'class': 'form-control'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Categoria'}),
            'imagen': CustomClearableFileInput(attrs={'class': 'form-control'}),
        }

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = proveedor
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'telefono': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
            'pagina': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Página Web'}),
            'imagen': CustomClearableFileInput(attrs={'class': 'form-control'}),
        }

        
class ClienteForm(forms.ModelForm):
    class Meta:
        model = clientes
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'a_paterno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido Paterno'}),
            'a_materno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido Materno'}),
            'nit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'NIT'}),
            'telefono': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
        }


class EmpleadoForm(forms.ModelForm):
    ESTADOS_CIVIL_OPCIONES = [
        ('', 'Seleccione su estado civil'),  # opción por defecto
        ('Soltero', 'Soltero'),
        ('Casado', 'Casado'),
        ('Divorciado', 'Divorciado'),
        ('Viudo', 'Viudo'),
    ]
    
    estado_civil = forms.ChoiceField(
        choices=ESTADOS_CIVIL_OPCIONES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True,
        label='Estado Civil'
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control password-toggle', 'placeholder': 'Contraseña'}),
        required=True,
        label='Contraseña'
    )

    class Meta:
        model = Empleado
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'a_paterno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido Paterno'}),
            'a_materno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido Materno'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
            'profesion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Profesion'}),
            'cargo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cargo'}),
            'nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control','placeholder':'Fecha de nacimiento'}),
            'ingreso': forms.DateInput(attrs={'type': 'date', 'class': 'form-control','placeholder': 'Fecha de ingreso'}),
            'sueldo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
        }