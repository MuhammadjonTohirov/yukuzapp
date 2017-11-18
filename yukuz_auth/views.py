from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from jsonpickle import json
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from yukuz_auth.models import Person, Driver
from yukuz_auth.serializers import PersonSerializers, UserSerializers, DriverSerializers


class PersonList(generics.ListAPIView, generics.ListCreateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializers
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def perform_create(self, serializer):
        avatar = self.request.data.get('image')
        # avatar = avatar.thumbnail(avatar.width / 2, avatar.height / 2, avatar.ANTIALIAS)
        # Person.objects.get_or_create(ssn=self.request.data['ssn'], phone_number=self.request.data['phone_number'],
        #                              user=self.request.user, image=avatar)
        serializer.save(user=self.request.user, ssn=self.request.data['ssn'],
                        phone_number=self.request.data['phone_number'], image=avatar)


class PersonDetails(generics.RetrieveUpdateAPIView, generics.RetrieveAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializers


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def get_id(request):
    user = User.objects.get(pk=request.user.id)
    person = Person.objects.get(user=user)
    dicti = {"first_name": str(user.first_name), "last_name": str(user.last_name), "ssn": str(person.ssn),
             "phone": str(person.phone_number), "image": str(person.image)}

    return HttpResponse(json.dumps(dicti))


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers


class DriverView(generics.CreateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializers
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def perform_create(self, serializer):
        driver_license_img = self.request.data.get('image')
        serializer.save(driver=self.request.user, car=self.request.data['car'], driver_license=driver_license_img)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers


def create(usr):
    user = User(
        email=usr['email'],
        username=usr['username'], first_name=usr['first_name'], last_name=usr['last_name'])
    user.set_password(usr['password'])
    try:
        user.save()
        return user
    except:
        return False


class RegisterView(generics.CreateAPIView, generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializers

    def perform_create(self, serializer):
        data = self.request.data
        create(data)

    def perform_update(self, serializer, id1=0):
        if self.request.auth is not None:
            first_name = self.request.data['first_name']
            last_name = self.request.data['last_name']
            passwd = self.request.data['password']
            user = User.objects.filter(pk=self.request.user.id).get()
            user.set_password(passwd)
            user.first_name = first_name
            user.last_name = last_name
            user.email = self.request.data['email']
            # user.username = username
            User.save(user)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
