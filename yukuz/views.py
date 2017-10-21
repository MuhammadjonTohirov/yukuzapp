import json

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, viewsets, status
from rest_framework.response import Response

from yukuz.api.permissions import IsStaffOrTargetUser, AllowAny
from yukuz.serialisers import PersonSerializers, VehicleTypeSerializers, UserSerializers
from yukuz.models import Person, VehicleType


# Create your views here.
class PersonList(generics.ListAPIView, generics.ListCreateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializers

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class VehicleTypeList(generics.ListAPIView, generics.CreateAPIView):
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


@csrf_exempt
def default_view(request):
    if request.method == "GET":
        try:
            q = request.GET['q']
            return HttpResponse(q)
        except:
            q = "no"
        return HttpResponse(q)
    if request.method == "POST":
        # Person.objects.create()
        q = request.POST.get('q', "nothing")
        return HttpResponse(q)
    return HttpResponse("...")


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    # def get_permissions(self):
    #     # allow non-authenticated user to create via POST
    #     return (AllowAny() if self.request.method == 'POST' or 'GET'
    #             else IsStaffOrTargetUser),


class RegisterView(generics.ListCreateAPIView):
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
        return (AllowAny() if self.request.method == 'POST'
                else IsStaffOrTargetUser()),


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
