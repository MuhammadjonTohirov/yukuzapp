from django.utils.encoding import force_text
from rest_framework import serializers, status
from rest_framework.exceptions import APIException, ErrorDetail
from django.utils.translation import ugettext_lazy as _
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict
from Utilites.Utility import ValidationError

from yukuz_firebase.models import MobDevice


class DevSerializer(serializers.ModelSerializer):
    device = serializers.CharField(max_length=30)
    is_driver = serializers.BooleanField()
    token = serializers.CharField(max_length=150)

    class Meta:
        model = MobDevice
        fields = ('device', 'is_driver', 'token', 'type')

    def is_valid(self, raise_exception=False):
        response = super().is_valid(raise_exception)
        return response

    # @staticmethod
    def validate_token(self, token):
        dev = None
        try:
            dev = MobDevice.objects.get(token=token)
            if dev is not None:
                self.raise_error(token)
        except:
            if dev is not None:
                self.raise_error(token)
            return token

    def raise_error(self, token):
        raise ValidationError({
            'token': token,
            'message': 'The device has been registered already'
        })
