import os
import sys
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime
from chat.helper import resizeUploadedImage
from django_resized import ResizedImageField

class _Abstract(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        
# Creation du user manager.
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, name, phone, password, **extra_fields):
        values = [email, name, phone]
        field_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))
        for field_name, value in field_value_map.items():
            if not value:
                raise ValueError('The {} value must be set'.format(field_name))

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            name=name,
            phone=phone,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, name, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_admin', False)
        return self._create_user(email, name, phone, password, **extra_fields)

    def create_superuser(self, email, name=None, phone=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, name, phone, password, **extra_fields)


def upload_to(instance, filename):
    now = timezone.now()
    base, extension = os.path.splitext(filename.lower())
    milliseconds = now.microsecond // 1000
    return f"images/users/{instance.pk}/profile-thumbnail/{base}-profile-{milliseconds}{extension}"

def nameFile(instance, filename):
    # resizeUploadedImage(instance,500,500)
    now = timezone.now()
    base, extension = os.path.splitext(filename.lower())
    milliseconds = now.microsecond // 1000
    return f"images/users/{instance.pk}/profile/{base}-profile-{milliseconds}{extension}"
class User(AbstractBaseUser):
    email = models.CharField(
        unique=True,
        blank=False,
        max_length=50
    )
    name = models.CharField(max_length=150, null=True)
    phone = models.CharField(max_length=50, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    # image = models.ImageField(upload_to=nameFile, blank=True, null=True)
    image_url = ResizedImageField(size=[600, 600],crop=['middle', 'center'], quality=75, upload_to=upload_to, force_format='PNG', blank=True, null=True)
    about = models.TextField(blank=True, null=True)

    is_active = models.BooleanField(default=True) #pour dire l'utilisateur est actif
    is_staff = models.BooleanField(default=False) # pour savoir si l'utilisateur a access au panneau d'administration par defaut
    is_admin = models.BooleanField(default=False) # pour savoir si le user a les droits d'administration
    is_superuser = models.BooleanField(default=False)
    
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = "email" #pour dire que c'est qvec se champs qu'on va s'authentifier
    #REQUIRED_FIELDS ="" #mettre les noms des champs qui vont etre obligatoire [""]
    # def get_full_name(self):
    #     return self.name

    # def get_short_name(self):
    #     return self.name.split()[0]
    def has_perm(self, perm, obj=None):
           return self.is_admin

    def has_module_perms(self, app_label):
       return self.is_admin

class Message(_Abstract):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    content = models.TextField(null=True)