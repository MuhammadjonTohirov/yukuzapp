from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.
from yukuz_oauth.models import Person, Driver
from .models import UUser
# from .forms import UserLoginForm, UserCreationForm


class UserAdmin(BaseUserAdmin):
    list_display = ('phone_number', 'is_admin', 'is_staff')
    # add_form = UserCreationForm
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {
            'fields': ('phone_number', 'password')
        }),
        ('Permissions', {
            'fields': ('is_admin',)
        })
    )
    # readonly_fields = ('date',)
    auto_now_add = True
    search_fields = ('phone_number', 'is_staff', 'is_admin')
    ordering = ('phone_number', 'is_admin')
    filter_horizontal = ()


class DriverAdmin(admin.ModelAdmin):
    list_display = ['driver', 'reg_date']


class PersonAdmin(admin.ModelAdmin):
    list_display = ['user', 'ssn', 'joined_date']


admin.site.unregister(Group)
admin.site.register(UUser)
admin.site.register(Person, PersonAdmin)
admin.site.register(Driver, DriverAdmin)

