from rest_framework import serializers

from firebase.models import MobDevice


class DevSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobDevice
        fields = ('device', 'user_id', 'is_driver', 'dev_version', 'type')
