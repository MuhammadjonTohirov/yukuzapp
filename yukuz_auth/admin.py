from django.contrib import admin

# Register your models here.
from yukuz_auth.models import Person, Driver


class DriverAdmin(admin.ModelAdmin):
    list_display = ['driver', 'reg_date']


class PersonAdmin(admin.ModelAdmin):
    list_display = ['user', 'ssn', 'joined_date']


admin.site.register(Person, PersonAdmin)
admin.site.register(Driver, DriverAdmin)
