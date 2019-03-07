from rest_framework import serializers

from yukuz_firebase.models import MobDevice


class DevSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobDevice
        fields = ('device', 'is_driver', 'token', 'type')
