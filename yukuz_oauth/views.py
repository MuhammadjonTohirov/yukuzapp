import json
from os.path import basename

from yukuz_oauth.models import UUser
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from yukuz_main.models import DriverRate
from yukuz_oauth.models import Person, Driver
from yukuz_oauth.serializers import PersonSerializers, UserSerializers, DriverSerializers, LoginSerializer

from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.compat import coreapi, coreschema
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema
from rest_framework.views import APIView


class UserDetail(generics.RetrieveAPIView):
    queryset = UUser.objects.all()
    serializer_class = UserSerializers


class UserList(generics.ListAPIView):
    queryset = UUser.objects.all()
    serializer_class = UserSerializers


class RegisterAndUpdateView(generics.CreateAPIView, generics.UpdateAPIView):
    queryset = UUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializers

    def perform_create(self, serializer):
        data = self.request.data
        create(data)

    def perform_update(self, serializer):
        if self.request.auth is not None:
            print("update user value")
            phone_number = self.request.data['phone_number']
            password = self.request.data['password']
            user = UUser.objects.filter(pk=self.request.user.id).get()
            user.set_password(password)
            user.phone_number = phone_number
            UUser.save(user)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


def create(usr):
    user = UUser(phone_number=usr['phone_number'])
    user.set_password(usr['password'])
    user.is_staff = True
    try:
        user.save()
        return True
    except:
        return False


class Login(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = LoginSerializer
    if coreapi is not None and coreschema is not None:
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="phone_number",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Phone number",
                        description="Valid phone number for authentication",
                    ),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Password",
                        description="Valid password for authentication",
                    ),
                ),
            ],
            encoding="application/json",
        )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


obtain_auth_token = Login.as_view()


class PersonView(generics.ListAPIView, generics.ListCreateAPIView):
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
