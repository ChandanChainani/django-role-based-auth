from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import AbstractUser, Permission

from .managers import CustomUserManager

class Role(models.Model):
    name = models.CharField(max_length=255)
    permissions = models.ManyToManyField(Permission)

    def __str__(self):
        return self.name

class User(AbstractUser):
    email = models.EmailField(error_messages={'unique': 'A user with that email already exists.'}, blank=True, max_length=254, unique=True, verbose_name='email address')
    username = models.CharField(help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, validators=[UnicodeUsernameValidator()], verbose_name='username')

    roles = models.ManyToManyField(Role, blank=True)
    permissions = models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='permissions')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    @property
    def user_permissions(self):
        return self.permissions
