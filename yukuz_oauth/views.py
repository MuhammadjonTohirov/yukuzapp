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
from Utilites.Utility import YResponse


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


class PersonView(generics.ListAPIView, generics.ListCreateAPIView, generics.UpdateAPIView):
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
        return YResponse.failure_response("cannot create")

    def patch(self, request, *args, **kwargs):
        person_list = Person.objects.filter(user=request.user)
        number_of_person_user_id = person_list.count()
        self.serializer_class = PersonSerializers(data=self.request.data, user=request.user)
        if number_of_person_user_id == 1:
            try:
                Person.objects.update(user=request.user, ssn=request.data['ssn'], image=request.data['image'])
                return YResponse.success_response("person updated successfully")
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
            context = {"status": False}
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
                        'phone_number': person.phone_number,
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
                    'phone_number': person.phone_number,
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
                  "phone": str(person.phone_number),
                  "image": str(person.image)}

    return HttpResponse(json.dumps(dictionary))
