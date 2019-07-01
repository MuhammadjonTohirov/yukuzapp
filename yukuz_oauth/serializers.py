from rest_framework.response import Response

from yukuz_oauth.models import UUser
from yukuz_oauth.models import Person, Driver

from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers, status


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UUser
        fields = ('password', 'username',)
        write_only_fields = ('password',)
        read_only_fields = ('is_staff', 'is_superuser', 'date_joined',)

    def restore_object(self, attrs, instance=None):
        user = super(UserSerializer, self).restore_object(attrs, instance)
        user.set_password(attrs['password'])
        return user


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = UUser

        fields = ('id',
                  'username')

    def update(self, instance, validated_data):
        instance.password = validated_data.get('password', instance.password)
        instance.save()
        return instance


class PersonSerializers(serializers.ModelSerializer):
    ssn = serializers.IntegerField(min_value=0, required=True)
    image = serializers.ImageField(required=True)

    def __init__(self, user, **kwargs):
        super().__init__(**kwargs)
        self.user = user
        self.status = False

    def create(self, validated_data):
        print("create a person serializer")

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
        fields = ['ssn', 'image', 'first_name', 'last_name', 'email']


class DriverSerializers(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['description', 'driver_license', "is_active", "reg_date"]


class LoginSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    username = serializers.CharField(label=_("Phone number"))
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            print(user)
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
