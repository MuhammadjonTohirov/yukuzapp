from django.contrib import admin

# Register your models here.
from mfirebase.models import DeviceType, MobDevice


class DeviceAdmin(admin.ModelAdmin):
    list_display = ['device', 'dev_version']
    list_filter = ['is_driver', 'type']


admin.site.register(DeviceType)
admin.site.register(MobDevice, DeviceAdmin)
