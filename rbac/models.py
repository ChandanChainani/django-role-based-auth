from django.db import models
from django.contrib import auth
from django.contrib.auth import models as auth_models, validators, base_user
from django.utils import timezone

from .managers import CustomUserManager

from django.core.exceptions import PermissionDenied
def _user_has_perm(user, perm, obj):
    """
    A backend can raise `PermissionDenied` to short-circuit permission checking.
    """
    for backend in auth.get_backends():
        if not hasattr(backend, 'has_perm'):
            continue
        try:
            if backend.has_perm(user, perm, obj):
                return True
        except PermissionDenied:
            return False
    return False

def _user_has_module_perms(user, app_label):
    """
    A backend can raise `PermissionDenied` to short-circuit permission checking.
    """
    for backend in auth.get_backends():
        if not hasattr(backend, 'has_module_perms'):
            continue
        try:
            if backend.has_module_perms(user, app_label):
                return True
        except PermissionDenied:
            return False
    return False

class Role(models.Model):
    name = models.CharField(max_length=255)
    permissions = models.ManyToManyField(auth_models.Permission)

class User(base_user.AbstractBaseUser):
    email = models.EmailField(error_messages={'unique': 'A user with that email already exists.'}, blank=True, max_length=254, unique=True, verbose_name='email address')
    password = models.CharField(max_length=128, verbose_name='password')
    username = models.CharField(help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, validators=[validators.UnicodeUsernameValidator()], verbose_name='username')
    first_name = models.CharField(blank=True, max_length=150, verbose_name='first name')
    last_name = models.CharField(blank=True, max_length=150, verbose_name='last name')
    is_active = models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')
    is_staff = models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')
    is_superuser = models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='date joined')
    last_login = models.DateTimeField(blank=True, null=True, verbose_name='last login')

    groups = models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')
    roles = models.ManyToManyField(Role, blank=True)
    permissions = models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='permissions')

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    @property
    def user_permissions(self):
        return self.permissions

    def has_perm(self, perm, obj=None):
        """
        Return True if the user has the specified permission. Query all
        available auth backends, but return immediately if any backend returns
        True. Thus, a user who has permission from a single auth backend is
        assumed to have permission in general. If an object is provided, check
        permissions for that object.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        # Otherwise we need to check the backends.
        return _user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        """
        Return True if the user has each of the specified permissions. If
        object is passed, check if the user has all required perms for it.
        """
        return all(self.has_perm(perm, obj) for perm in perm_list)

    def has_module_perms(self, app_label):
        """
        Return True if the user has any permissions in the given app label.
         Use similar logic as has_perm(), above.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)
