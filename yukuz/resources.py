from tastypie import fields
from tastypie.authentication import BasicAuthentication, Authentication
from tastypie.authorization import Authorization, DjangoAuthorization, ReadOnlyAuthorization
from tastypie.resources import ModelResource
from yukuz.models import Person, PostOrder, PickedOrder, Driver
from yukuz.models import VehicleType, Car
from django.contrib.auth.models import User


# authorization by django admin
class UserAuthResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'auth'
        excludes = ['email', 'is_superuser']
        allowed_methods = ['get', 'post']  # accepts only get request from client
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()


class UserList(ModelResource):
    class Meta:
        queryset = Person.objects.all()  # get all users list
        resource_name = 'users'
        allowed_methods = ['get', 'post']  # accepts only get request from client
        authorization = BasicAuthentication()  # gives ReadOnlyAuthorization


class VehicleTypeList(ModelResource):
    class Meta:
        queryset = VehicleType.objects.all()  # get all vehicle types list
        resource_name = 'vehicles'
        allowed_methods = ['get', 'post', 'delete']
        authorization = Authorization()  # gives ReadOnlyAuthorization


class PostOrderList(ModelResource):
    order_by = fields.ForeignKey(UserList, 'order_by')

    # PostOrder.objects.all().filter().update(is_picked=True)

    class Meta:
        queryset = PostOrder.objects.all()
        resource_name = 'posts'
        filtering = {'title', all}
        authorization = Authorization()  # gives ReadOnlyAuthorization


class VehiclesList(ModelResource):
    vehicle_type = fields.ForeignKey(VehicleTypeList, 'car_type')

    class Meta:
        queryset = Car.objects.all()
        resource_name = 'cars'


class DriverList(ModelResource):
    driver = fields.OneToOneField(UserList, 'driver')
    vehicle = fields.ForeignKey(VehiclesList, 'car')

    class Meta:
        queryset = Driver.objects.all()
        resource_name = 'drv'


class PickedOrderList(ModelResource):
    order = fields.ForeignKey(PostOrderList, 'order')
    picked_by_driver = fields.ForeignKey(DriverList, 'picked_by')

    class Meta:
        queryset = PickedOrder.objects.all()
        resource_name = 'picked-orders'
        fields = ['id', 'order']
        filtering = {'id', all}
