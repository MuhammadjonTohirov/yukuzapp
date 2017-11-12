import json

from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from yukuz.api.permissions import IsStaffOrTargetUser, AllowAny
from yukuz.serialisers import PersonSerializers, VehicleTypeSerializers, UserSerializers, DevSerializer, \
    PostOrderSerializers, PickedOrderSerializers
from yukuz.models import Person, VehicleType, MobDevice, PostOrder, PickedOrder, PriceClass


# Create your views here.
class PersonList(generics.ListAPIView, generics.ListCreateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializers
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def perform_create(self, serializer):
        avatar = self.request.data.get('image')
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


class VehicleTypeList(generics.ListAPIView, generics.CreateAPIView):
    queryset = VehicleType.objects.all()
    serializer_class = VehicleTypeSerializers
    permission_classes = ((AllowAny,))


class CreateDevice(generics.ListAPIView, generics.CreateAPIView):
    queryset = MobDevice.objects.all()
    serializer_class = DevSerializer

    def get(self, request, *args, **kwargs):
        # header = request.META['HTTP_AUTHORIZATION']
        q = MobDevice.objects.all()
        ser = DevSerializer(q, many=True)
        return Response(ser.data)

        # @api_view(['POST', 'GET'])


# def CreateDevice(request):
#     if (request.method == 'GET'):
#         devices = MobDevice.objects.all()
#         serializer = DevSerializer(devices, many=True)
#         # token = request.META['HTTP_AUTHORIZATION']
#         return Response(serializer.data)
#     if (request.method == 'POST'):
#         ser = DevSerializer(data=request.data)
#         if ser.is_valid():
#             ser.save()
#             return Response(ser.data, status=status.HTTP_201_CREATED)
#         return Response(ser.error_messages, status=status.HTTP_400_BAD_REQUEST)


def read_token(request):
    token = False

    if token:
        return HttpResponse(token)
    else:
        return HttpResponse(str(request.META['HTTP_AUTHORIZATION']))


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


@permission_classes((IsAuthenticated,))
@csrf_exempt
def update_post(request):
    if request.method == 'POST':
        try:
            id = request.POST['id']
            cancel = request.POST['cancel']
            price = request.POST['price']
            deadline = request.POST['deadline']
            descr = request.POST['description']
            order = PostOrder.objects.get(id=id)
            order.is_cancelled = bool(cancel)
            order.estimated_price = price
            order.deadline = deadline
            order.description = descr
            order.save()
            return HttpResponse("updated")
        except:
            return HttpResponse(status=status.HTTP_304_NOT_MODIFIED)
    else:
        return HttpResponse("Send POST request")


class PostsList(generics.ListAPIView, generics.CreateAPIView):
    def get(self, request, *args, **kwargs):
        try:
            type = request.GET['id']
            if type is "1":
                queryset = PostOrder.objects.filter(order_by__user=request.user, is_picked=False).all()
                serializer_class = PostOrderSerializers(queryset, many=True)

                for x in serializer_class.data:
                    t = x['currency_type']
                    currency = PriceClass.objects.get(id=t)
                    x.update({'currency': currency.title})

                json_data = JSONRenderer().render(serializer_class.data)

                return HttpResponse(json_data)
            elif type is "2":
                return HttpResponse("OK")
            else:
                return Response(status.HTTP_204_NO_CONTENT)
        except:
            return Response(status.HTTP_204_NO_CONTENT)

    def post(self, request, *args, **kwargs):
        serializer_class = PostOrderSerializers(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            PostOrder.objects.create(order_by=Person.objects.get(user=request.user), **serializer_class.validated_data)
            return Response("{\"status\":\"created\"}")
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers


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


class PickedOrderList(generics.ListAPIView):
    queryset = PickedOrder.objects.all()
    serializer_class = PickedOrderSerializers


# class UploadAvatar(generics.CreateAPIView):
#     queryset = UserAvatar.objects.all()
#     serializer_class = UploadAvatarSerializer
#     parser_classes = (MultiPartParser, FormParser, JSONParser)
#
#     def perform_create(self, serializer):
#         token = Token.objects.filter(key=self.request._auth).all()[0]
#
#         if token is None:
#             prk = self.request._user.id
#         else:
#             prk = token.user
#         if self.request.data.get('image') is not None:
#             avatar = self.request.data.get('image')
#             serializer.save(owner=prk, image=avatar)
#         else:
#             serializer.save(owner=prk)
def getPriceClass(request):
    from django.core import serializers
    queryset = PriceClass.objects.all()
    ser = serializers.serialize("json", queryset)
    # jsondata = JSONRenderer().render(data=ser)
    return HttpResponse(ser)
