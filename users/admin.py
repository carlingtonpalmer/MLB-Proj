from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from . import models

# Register your models here.


class UserAdmin(BaseUserAdmin):

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )


    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields' : ('email', 'password1', 'password2', 'first_name', 'last_name')
        }),
    )

    list_display = ('email', 'first_name', 'last_name', 'phone_no', 'provider', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_active',)
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(models.User, UserAdmin)
admin.site.register(models.ConfirmEmail)

