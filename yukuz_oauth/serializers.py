from rest_framework.response import Response

from yukuz_oauth.models import UUser
from yukuz_oauth.models import Person, Driver

from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers, status


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UUser
        fields = ('password', 'phone_number',)
        write_only_fields = ('password',)
        read_only_fields = ('is_staff', 'is_superuser', 'date_joined',)

    def restore_object(self, attrs, instance=None):
        user = super(UserSerializer, self).restore_object(attrs, instance)
        user.set_password(attrs['password'])
        return user


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = UUser
        fields = ('id', 'phone_number')


class PersonSerializers(serializers.ModelSerializer):
    ssn = serializers.IntegerField(min_value=0, required=True)
    image = serializers.ImageField(required=True)

    def __init__(self, user, **kwargs):
        super().__init__(**kwargs)
        self.user = user
        self.status = False

    def create(self, validated_data):
        print("create a person serializer")
        ssn = validated_data.get('ssn')

        return Person.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     print("updating the person serializer")
    #     instance.ssn = validated_data.get('ssn', instance.ssn)
    #     instance.image = validated_data.get('image', instance.image)
    #     instance.save()
    #
    #     return instance

    def is_valid(self, raise_exception=False):
        super().is_valid(raise_exception=raise_exception)
        number_of_persons = Person.objects.filter(user=self.user).count()
        if number_of_persons > 0:
            self._errors['message'] = 'person has been created already'
            return False
        return True

    class Meta:
        model = Person
        fields = ['ssn', 'image']

        # exclude = ['user']


class DriverSerializers(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['description', 'driver_license']


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(label=_("Phone number"))
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')

        if phone_number and password:
            user = authenticate(request=self.context.get('request'),
                                phone_number=phone_number, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "phone number" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
