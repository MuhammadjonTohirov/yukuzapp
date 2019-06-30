import json
from os.path import basename

from django.contrib import auth

from yukuz_main.views import ListAPIView
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
from Utilites.Utility import YResponse


class UserDetail(generics.RetrieveAPIView):
    queryset = UUser.objects.all()
    serializer_class = UserSerializers


class UserList(ListAPIView):
    queryset = UUser.objects.all()
    serializer_class = UserSerializers


@api_view(['POST'])
@permission_classes((AllowAny,))
def register(request):
    serializer = UserSerializers(data=request.data)
    if serializer.is_valid():
        create(request.data)
        return YResponse.success_response(serializer.data)
    return YResponse.failure_response(serializer.errors)


@api_view(['PATCH'])
@permission_classes((IsAuthenticated,))
def update_password(request):
    instance = UUser.objects.get(username=request.user.username)

    password = request.data.get('password')
    if password is None:
        return YResponse.failure_response('password field is required')
    else:
        instance.set_password(password)
        instance.save()
        return YResponse.success_response(instance.dict())


def create(usr):
    user = UUser(username=usr['username'])
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
                    name="username",
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
        print(serializer.error_messages)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key})


obtain_auth_token = Login.as_view()


class PersonList(ListAPIView, generics.ListCreateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializers
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def perform_create(self, serializer):
        avatar = self.request.data.get('image')
        serializer.save(user=self.request.user, ssn=self.request.data['ssn'],
                        username=self.request.data['username'], image=avatar)


class PersonView(ListAPIView, generics.ListCreateAPIView, generics.UpdateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializers
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request, *args, **kwargs):
        print("on post")
        user = request.user
        serializer_class = PersonSerializers(data=request.data, user=user)

        number_of_person_by_ssn = Person.objects.filter(ssn=request.data['ssn']).count()

        if number_of_person_by_ssn == 0:
            if serializer_class.is_valid(raise_exception=True):
                serializer_class.save()
                return YResponse.created_response(serializer_class.data)
            return YResponse.failure_response(serializer_class.errors)
        else:
            return YResponse.failure_response({
                'message': 'The person with ssn is exists'
            })

    def patch(self, request, *args, **kwargs):

        person_list = Person.objects.filter(user_id=request.user.id)
        number_of_person_user_id = person_list.count()
        self.serializer_class = PersonSerializers(data=self.request.data, user=request.user)
        if number_of_person_user_id == 1:
            try:
                person = person_list[0]
                person.ssn = request.data.get('ssn', person.ssn)
                person.image = request.data.get('image', person.image)
                person.first_name = request.data.get('first_name', person.first_name)
                person.last_name = request.data.get('last_name', person.last_name)
                person.email = request.data.get('email', person.email)
                person.save()
                import json
                print(person.dict())
                return YResponse.success_response(person.dict())
            except:
                return YResponse.failure_response("Bad parameters")
        else:
            return YResponse.failure_response("The person not created before")


class DriverView(generics.CreateAPIView, generics.ListAPIView, generics.UpdateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializers
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def perform_create(self, serializer):
        driver_license_img = self.request.data.get('driver_license')
        serializer.save(driver=Person.objects.get(user=self.request.user), description=self.request.data['description'],
                        driver_license=driver_license_img)

    def get(self, request, *args, **kwargs):
        try:
            purpose = request.GET['id']
            context = {"status": 400}
            if purpose == u'1':
                total_data = []
                drivers = request.GET.getlist('d_id')
                for d in drivers:
                    driver = Driver.objects.get(driver__user=d, )
                    person = driver.driver
                    user = driver.driver.user

                    rate = DriverRate.objects.filter(star_for__assigned_to=driver, star_for__is_finished=True).count()
                    context = {
                        'license_image': driver.driver_license.url,
                        'image': person.image.url,
                        'description': driver.description,
                        'image_title': basename(driver.driver_license.url),
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'ssn': person.ssn,
                        'email': user.email,
                        'username': person.username,
                        'rate': rate
                    }
                    total_data.append(context.copy())
                return HttpResponse(json.dumps(total_data))
            elif purpose == "2":
                driver = Driver.objects.get(driver__user=request.user)

                person = driver.driver
                user = driver.driver.user
                rate = DriverRate.objects.filter(star_for__assigned_to=driver, star_for__is_finished=True).count()
                context = {
                    'license_image': driver.driver_license.url,
                    'image': person.image.url,
                    'description': driver.description,
                    'image_title': basename(driver.driver_license.url),
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'ssn': person.ssn,
                    'email': user.email,
                    'username': person.username,
                    'rate': rate
                }

            return HttpResponse(json.dumps(context))
        except Exception as ex:
            return HttpResponse(ex)

    def update(self, request, *args, **kwargs):
        context = {'success': False, 'driver_mode': False}
        try:
            driver = Driver.objects.get(driver__user=request.user)
            driver.is_active = True if driver.is_active is False else False
            driver.save()
            context = {'success': True, 'driver_mode': driver.is_active}
            return HttpResponse(json.dumps(context))
        except:
            context['driver_mode'] = False
            return HttpResponse(json.dumps(context))

    def handle_exception(self, exc):
        context = {'success': False, 'driver_mode': False, 'exception': str(exc)}
        return HttpResponse(json.dumps(context))


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def get_id(request):
    user = UUser.objects.get(pk=request.user.id)
    person = Person.objects.get(user=user)
    dictionary = {"first_name": str(user.first_name),
                  "last_name": str(user.last_name),
                  "ssn": str(person.ssn),
                  "phone": str(person.username),
                  "image": str(person.image)}

    return HttpResponse(json.dumps(dictionary))
