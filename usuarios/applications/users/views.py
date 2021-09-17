from django.shortcuts import render
from django.core.mail import send_mail
from django.views.generic import CreateView, ListView,View
from django.views.generic.edit import FormView
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import (UserRegisterForm, LoginForm, UpdatePasswordForm, VerificationForm)
from .models import User
from .functions import code_generator





class UserRegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm

    success_url = '/'

    def form_valid(self, form):
        #generamos el codigo
        codigo = code_generator()

        usuario = User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            nombres=form.cleaned_data['nombres'],
            apellidos=form.cleaned_data['apellidos'],
            genero=form.cleaned_data['genero'],
            code_registro=codigo

        )

        #enviar codigo al email del usuario
        asunto = 'Confirmacion de Email'
        mensaje = 'Codigo de verificacion: ' + codigo
        email_remitente= 'calatravabrian2@gmail.com'

        #es un array porque se pueden enviar a varios correos
        send_mail(asunto, mensaje, email_remitente, [form.cleaned_data['email'],])

        #redirigir a pantalla de validacion
        


        return HttpResponseRedirect(reverse('users_app:user-verification', kwargs={'pk': usuario.id}))




class LoginUser(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home_app:home')

    def form_valid(self, form):
        user = authenticate(
            self.request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password2']

        )
        login(self.request, user)


        return super(LoginUser, self).form_valid(form)




class LogOutView(View):
    
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('users_app:login'))






class UpdatePassword(LoginRequiredMixin, FormView):
    template_name = 'users/update_password.html'
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('users_app:login')
    login_url = reverse_lazy('users_app:login')

    def form_valid(self, form):
        #con esto obtengo el usuario que se encuentre en sesion
        usuario = self.request.user
        user = authenticate(
            username=usuario.username,
            password=form.cleaned_data['password']

        )

        if user:
            new_password= form.cleaned_data['password_nueva']
            usuario.set_password(new_password)
            usuario.save()
        logout(self.request)



        return super(UpdatePassword, self).form_valid(form)


class CodeVerificationView(FormView):
    template_name = 'users/verification.html'
    form_class = VerificationForm
    success_url = reverse_lazy('users_app:login')

    #con esto le decimos que mande los kwargs al formulario con el cual estamos trabajando
    def get_form_kwargs(self):
        kwargs= super(CodeVerificationView, self).get_form_kwargs()
        kwargs.update({
            'pk': self.kwargs['pk'],
        })
        return kwargs


    def form_valid(self, form):
        
        User.objects.filter(
            id=self.kwargs['pk']
        ).update(
            is_active=True
        )


        return super(CodeVerificationView, self).form_valid(form)

