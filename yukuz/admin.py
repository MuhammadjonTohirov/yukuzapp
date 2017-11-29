from django.contrib import admin
from .models import VehicleType, Car, OrderImages
from .models import PostOrder, PickedOrder, PriceClass


# Register your models here.


class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']


class CarAdmin(admin.ModelAdmin):
    list_display = ['title', 'min_kg', 'max_kg', 'by_person', 'number']


class PostOrderAdmin(admin.ModelAdmin):
    list_display = ['post_title', 'source_address', 'destination_address', 'order_by', 'order_time']


class PickedOrderAdmin(admin.ModelAdmin):
    filter_horizontal = ('picked_by',)
    list_display = ['order', 'picked_time']


admin.site.register(PriceClass)
admin.site.register(OrderImages)
# admin.site.register(UserAvatar)
admin.site.register(VehicleType, VehicleTypeAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(PostOrder, PostOrderAdmin)
admin.site.register(PickedOrder, PickedOrderAdmin)
