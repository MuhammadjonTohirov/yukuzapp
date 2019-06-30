from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext, gettext_lazy as _
# Register your models here.
from yukuz_oauth.models import Person, Driver
from .models import UUser
from yukuz_oauth.forms import UUserChangeForm, UUserCreationForm


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'is_admin', 'is_staff', 'is_superuser', 'creation_date']
    add_form = UUserCreationForm
    form = UUserChangeForm
    add_form_template = 'admin/auth/user/add_form.html'
    change_user_password_template = None
    model = UUser

    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),

        (_('Permissions'), {'fields': ('is_admin', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')
        }),
        ('Permissions', {
            'fields': ('is_admin', 'is_staff', 'is_superuser')
        })
    )

    auto_now_add = True
    search_fields = ('username', 'is_staff', 'is_admin')
    ordering = ('username', 'is_admin')
    filter_horizontal = ()

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during user creation
        """
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)


class DriverAdmin(admin.ModelAdmin):
    list_display = ['driver', 'reg_date']


class PersonAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'image', 'ssn', 'joined_date']

    search_fields = ['ssn', 'first_name', 'last_name']
    list_filter = ['joined_date']


admin.site.unregister(Group)
admin.site.register(UUser, UserAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Driver, DriverAdmin)
