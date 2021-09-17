
from django import forms
from django.forms import forms
from  django import forms
from .models import User
from django.contrib.auth import authenticate, login,logout



class UserRegisterForm(forms.ModelForm):
    
    password1 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña'
            }
        )
    )

    password2 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repetir Contraseña'
            }
        )
    )

    class Meta:
        

        model = User
        fields = ('username','email','nombres','apellidos','genero')
    
    def clean_password2(self):
        if len(self.cleaned_data['password1']) < 6:
            self.add_error('password1', 'Laa contraseña debe ser mayor a 5 caracteres')
        elif self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self.add_error('password2', 'Las contraseñas no son iguales')


class LoginForm(forms.Form):

    username = forms.CharField(
        label='Username',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username'
            }
        )
    )

    password2 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña'
            }
        )
    )

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = self.cleaned_data['username']
        password = self.cleaned_data['password2']

        if not authenticate(username=username, password=password):
            raise forms.ValidationError('Los datos del usuario no son correctos')
        
        return self.cleaned_data


class UpdatePasswordForm(forms.Form):
    password = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña Actual'
            }
        )
    )
    password_nueva = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña nueva'
            }
        )
    )


class VerificationForm(forms.Form):
    code_enviado = forms.CharField(required=True)

    
    def __init__(self, pk,*args, **kwargs):
        self.id_user = pk
        super(VerificationForm, self).__init__(*args, **kwargs)
    

    def clean_code_enviado(self):
        codigo = self.cleaned_data['code_enviado']

        if len(codigo) == 6:
            #verificamos si el codigo y el id del usuario son validos
            activo = User.objects.cod_validator(
                self.id_user,
                codigo
            )

            if not activo:
                raise forms.ValidationError('El codigo es incorrecto')

        else:
            raise forms.ValidationError('El codigo es incorrecto')