from django.contrib import admin
from .models import Person
from .models import Driver
from .models import VehicleType, Car
from .models import PostOrder, PickedOrder


# Register your models here.
class PersonAdmin(admin.ModelAdmin):
    list_display = ['user', 'ssn', 'joined_date']


class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']


class CarAdmin(admin.ModelAdmin):
    list_display = ['car_type', 'min_kg', 'max_kg']


class DriverAdmin(admin.ModelAdmin):
    list_display = ['driver', 'reg_date']


class PostOrderAdmin(admin.ModelAdmin):
    list_display = ['title', 'source_address', 'destination_address', 'order_by', 'order_time']


class PickedOrderAdmin(admin.ModelAdmin):
    list_display = ['order', 'picked_by', 'picked_time']


admin.site.register(Person, PersonAdmin)
admin.site.register(VehicleType, VehicleTypeAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(PostOrder, PostOrderAdmin)
admin.site.register(PickedOrder, PickedOrderAdmin)
