from rest_framework import serializers

# from yukuz_firebase.models import MobDevice
from yukuz_main.models import VehicleType, Car, PostOrder, PickedOrder, Driver


class VehicleTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = VehicleType
        fields = ['id', 'title', 'description']


class CarSerializers(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['title', 'car_type', 'number', 'min_kg', 'max_kg']


class PostOrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = PostOrder
        fields = ('id', 'post_title', 'description', 'weigth', 'source_address',
                  'destination_address',
                  'order_time', 'deadline', 'currency_type', 'estimated_price',
                  'type_of_vehicle', 'is_cancelled')
        # exclude = []

class PostOrderSerializersForDriver(serializers.ModelSerializer):
    class Meta:
        model = PostOrder
        # fields = ('id', 'post_title', 'order_time', 'deadline', 'currency_type', 'estimated_price', 'order_by')
        exclude = ['is_cancelled']


class PickedOrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = PickedOrder
        fields = ['order', 'picked_by', 'picked_time']

# class UploadAvatarSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserAvatar
#         fields = ['owner', 'image']
