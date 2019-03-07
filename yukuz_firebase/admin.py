from django.contrib import admin

# Register your models here.
from yukuz_firebase.models import DeviceType, MobDevice


class DeviceAdmin(admin.ModelAdmin):
    list_display = ['device', 'token']
    list_filter = ['is_driver', 'type']


admin.site.register(DeviceType)
admin.site.register(MobDevice, DeviceAdmin)
