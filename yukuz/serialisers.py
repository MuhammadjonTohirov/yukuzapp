from django.contrib.auth.models import User, AbstractBaseUser
from rest_framework import serializers
from yukuz.models import Person, VehicleType, Car, Driver, PostOrder


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
    # person = serializers.PrimaryKeyRelatedField(many=False, queryset=Person.objects.all())

    # owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = User
        fields = ('id', 'username', 'email')
        # create(fields)
        # extra_kwargs = {'password': {'write_only': True}}
        # create(model)
        # model.set_password(AbstractBaseUser, make_password(fields[1]))


class PersonSerializers(serializers.ModelSerializer):
    avatar = serializers.ImageField(max_length=None, use_url=None)

    class Meta:
        model = Person
        fields = ['id', 'ssn', 'user', 'phone_number', 'avatar']


class VehicleTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = VehicleType
        fields = ['id', 'title', 'description']


class CarSerializers(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'car_type', 'description']


class DriverSerializers(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['id', 'driver', 'car']


class PostOrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = PostOrder
        fields = ['title', 'description', 'weigth', 'source_address', 'destination_address', 'is_picked', 'order_by',
                  'order_time']
