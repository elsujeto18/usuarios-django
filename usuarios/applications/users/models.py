from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models.fields import EmailField
# Create your models here.
from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    
    GENDER_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro')
    )

    username = models.CharField( max_length=10, unique=True)
    
    email = models.EmailField()
    nombres = models.CharField( max_length=30, blank=True)
    apellidos = models.CharField( max_length=30, blank=True)
    genero = models.CharField( max_length=1, choices=GENDER_CHOICES, blank=True)
    code_registro= models.CharField(max_length=6,blank=True)

    #AbstractBaseUser
    is_staff = models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects= UserManager()

    '''def get_short_name(self):
        return str(self.id) + ' - ' + self.username'''

    def __str__(self):
        return str(self.id) + ' - ' + self.username

        
    def get_full_name(self):
        return self.nombres +  ' ' + self.apellidos
    
