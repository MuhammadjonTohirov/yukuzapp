import json

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, viewsets
from yukuz.api.permissions import IsStaffOrTargetUser, AllowAny
from yukuz.serialisers import PersonSerializers, VehicleTypeSerializers, UserSerializers
from yukuz.models import Person, VehicleType


# Create your views here.
class PersonList(generics.ListAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializers

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class VehicleTypeList(generics.ListAPIView):
    queryset = VehicleType.objects.all()
    serializer_class = VehicleTypeSerializers


def create(usr):
    user = User(
        email=usr['email'],
        username=usr['username'], )
    user.set_password(usr['password'])
    try:
        user.save()
        return user
    except:
        return False


class UserList(generics.ListAPIView, generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers

    @csrf_exempt
    def post(self, request, **kwargs):
        data = str(str(request.data).replace("\'", "\""))
        d = json.loads(data)
        result = create(d)
        if result is False:
            return HttpResponse({'{\"created\":\"' + str(result) + '\"}': request.data})
        else:
            return HttpResponse({'{\"created\":\"' + str(result.id) + '\"}': request.data})

    def get_permissions(self):
        # allow non-authenticated user to create via POST
        return (AllowAny() if self.request.method == 'POST' or self.request.method == 'GET'
                else IsStaffOrTargetUser),


class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializers
    model = User

    def get_permissions(self):
        # allow non-authenticated user to create via POST
        return (AllowAny() if self.request.method == 'POST' or self.request.method == 'GET'
                else IsStaffOrTargetUser()),


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
