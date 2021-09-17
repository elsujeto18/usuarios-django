from django.db import models
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager, models.Manager):
    #lo que se coloca en el model, primero los campos del modelo User y esto igualado a las variables que recibe esa funcion
    def _create_user(self, username, email, password,  is_staff, is_superuser, is_active, **extra_fields):
        user = self.model(
            username=username,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active,
            **extra_fields
        )
        
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username,email,  password=None, **extra_fields):
        return self._create_user(username,email, password, False, False, False,**extra_fields )

        

    def create_superuser(self, username, email,  password=None, **extra_fields):
        return self._create_user(username, email, password,  True, True, True, **extra_fields)



    def cod_validator(self, id_usuario, cod_registro):
        if self.filter(id=id_usuario, code_registro=cod_registro).exists():
            return True
        else:
            return False