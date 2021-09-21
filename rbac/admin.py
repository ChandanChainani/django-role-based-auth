from django import forms
from django.contrib import admin
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from .models import User, Role

class CustomUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    email = forms.EmailField(
        label=_("Email address"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'}),
        help_text=_("Please enter a valid email address")
    )

    class Meta:
        model = User
        fields = ('email',)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'roles', 'permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    filter_horizontal = ('groups', 'roles', 'permissions',)
    add_form = CustomUserCreationForm
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff')

class RoleAdmin(admin.ModelAdmin):
    filter_horizontal = ('permissions',)

admin.site.register(Role, RoleAdmin)
