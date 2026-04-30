from django import forms
from .models import Calificacion
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CalificacionForm(forms.ModelForm):
    class Meta:
        model = Calificacion
        exclude = ['promedio']
        widgets = {
            'nombre_estudiante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo del estudiante'
            }),
            'identificacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de identificación'
            }),
            'asignatura': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la asignatura'
            }),
            'nota1': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0', 'max': '5', 'step': '0.1',
                'placeholder': '0.0 - 5.0'
            }),
            'nota2': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0', 'max': '5', 'step': '0.1',
                'placeholder': '0.0 - 5.0'
            }),
            'nota3': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0', 'max': '5', 'step': '0.1',
                'placeholder': '0.0 - 5.0'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        for campo in ['nota1', 'nota2', 'nota3']:
            nota = cleaned_data.get(campo)
            if nota is not None:
                if nota < 0 or nota > 5:
                    self.add_error(campo, 'La nota debe estar entre 0.0 y 5.0')
        return cleaned_data


class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'