from django.contrib.auth.models import User
from rest_framework import serializers

from yukuz_auth.models import Person, Driver


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password', 'first_name', 'last_name', 'email',)
        write_only_fields = ('password',)
        read_only_fields = ('is_staff', 'is_superuser', 'is_active', 'date_joined',)

    def restore_object(self, attrs, instance=None):
        # call set_password on user object. Without this
        # the password will be stored in plain text.
        user = super(UserSerializer, self).restore_object(attrs, instance)
        user.set_password(attrs['password'])
        return user


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

        # create(fields)
        # extra_kwargs = {'password': {'write_only': True}}
        # create(model)
        # model.set_password(AbstractBaseUser, make_password(fields[1]))


class PersonSerializers(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['ssn', 'phone_number', 'image', 'user']
        # exclude = ['user']


class DriverSerializers(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['driver', 'car', 'driver_license']
