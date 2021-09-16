from django.db import models
from django.contrib import auth
from django.utils import timezone

from .managers import CustomUserManager

class Role(models.Model):
    name = models.CharField(max_length=255)
    permissions = models.ManyToManyField(auth.models.Permission)

class User(auth.base_user.AbstractBaseUser):
    email = models.EmailField(error_messages={'unique': 'A user with that email already exists.'}, blank=True, max_length=254, unique=True, verbose_name='email address')
    password = models.CharField(max_length=128, verbose_name='password')
    username = models.CharField(help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, validators=[auth.validators.UnicodeUsernameValidator()], verbose_name='username')
    first_name = models.CharField(blank=True, max_length=150, verbose_name='first name')
    last_name = models.CharField(blank=True, max_length=150, verbose_name='last name')
    is_active = models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')
    is_staff = models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')
    is_superuser = models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='date joined')
    last_login = models.DateTimeField(blank=True, null=True, verbose_name='last login')

    groups = models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')
    roles = models.ManyToManyField(Role)
    permissions = models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='permissions')

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
