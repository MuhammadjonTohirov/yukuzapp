from rest_framework import serializers

from mfirebase.models import MobDevice


class DevSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobDevice
        fields = ('device', 'is_driver', 'dev_version', 'type')
