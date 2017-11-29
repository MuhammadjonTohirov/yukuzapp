import json

from django.contrib.auth.models import User
from django.core import serializers
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from mfirebase import notifications
from mfirebase.models import MobDevice
from yukuz.serialisers import VehicleTypeSerializers, \
    PostOrderSerializers, PickedOrderSerializers, CarSerializers, PostOrderSerializersForDriver
from yukuz.models import Person, VehicleType, PostOrder, PickedOrder, PriceClass, Driver, Car


# Create your views here.


class VehicleTypeList(generics.ListAPIView, generics.CreateAPIView):
    queryset = VehicleType.objects.all()
    serializer_class = VehicleTypeSerializers
    permission_classes = ((AllowAny,))


@permission_classes((IsAuthenticated,))
@csrf_exempt
def default_view(request):
    if request.method == "GET":
        try:
            print(request.user)
            contex = {"person": False, "driver": False, "is_alive": True, "driver_active": False}
            from rest_framework.authtoken.models import Token
            token = Token.objects.get(key=str(request.META['HTTP_AUTHORIZATION']).split(" ")[1])
            person = Person.objects.get(user=token.user)
            contex["person"] = True
            try:
                drvr = Driver.objects.get(driver=person)
                contex["driver"] = True
                contex["driver_active"] = drvr.is_active
                result = json.dumps(contex)
                return HttpResponse(result)
            except:
                result = json.dumps(contex)
                return HttpResponse(result)
        except Exception as ex:
            return HttpResponse(ex)
    return HttpResponse("You are nothing")


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
                queryset = PostOrder.objects.filter(is_cancelled=False, is_picked=False). \
                    exclude(order_by__user=request.user).all()
                serializer = PostOrderSerializersForDriver(queryset, many=True)

                for x in serializer.data:
                    t = x['currency_type']
                    currency = PriceClass.objects.get(id=t)
                    x.update({'currency': currency.title})
                    usr = x['order_by']
                    us = Person.objects.get(user=usr).user
                    x.update({'username': us.first_name + " " + us.last_name})
                json_data = JSONRenderer().render(serializer.data)
                return HttpResponse(json_data)
            else:
                return Response(status.HTTP_204_NO_CONTENT)
        except:
            return Response(status.HTTP_204_NO_CONTENT)

    def post(self, request, *args, **kwargs):
        serializer_class = PostOrderSerializers(data=request.data)
        context = {"success": False, "time": None}
        if serializer_class.is_valid(raise_exception=True):
            post = PostOrder.objects.create(order_by=Person.objects.get(user=request.user),
                                            **serializer_class.validated_data)
            # post = PostOrder.objects.all()[0]
            cars = Car.objects.filter(car_type=request.data['type_of_vehicle']).exclude(
                by_person=Person.objects.get(user=request.user)).all()
            total_data = []
            person = Person.objects.get(user=request.user)
            sender = ''
            for a in cars:
                devs = MobDevice.objects.filter(user_id__driver__is_active=True,
                                                user_id__driver=Driver.objects.get(driver=a.by_person)).all()
                # there is a logical error, I have to look at this function one more time later;
                device = ''
                for d in devs:
                    device = d.device
                order = request.data
                body = {"user_id": request.user.pk,
                        "image": str(person.image), "first_name": request.user.first_name,
                        "last_name": request.user.last_name,
                        "user_ssn": person.ssn, "user_email": request.user.email,
                        "user_number": person.phone_number, 'order_id': post.id, 'order': order}

                header = {"notif_type": "post_order"}

                sender = {'token': device, 'title': (header), 'body': (body)}
                context["success"] = True
                context["time"] = str(post.order_time)
                print(sender)
                notifications.send_notification(sender)

            return HttpResponse(json.dumps(sender))
        return HttpResponse(json.dumps(context))


class CarView(generics.ListAPIView, generics.CreateAPIView, generics.DestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializers

    # def perform_create(self, serializer):
    # car_image = self.request.data.get('image')
    # Car.objects.create(title=self.request.data['title'], car_type=self.request.data['c_type'],
    #                    number=self.request.data['number'], min_kg=self.request.data['min_kg'],
    #                    max_kg=self.request.data['max_kg'], by_person=self.request.user, image=car_image)
    def get(self, request, *args, **kwargs):
        queryset = Car.objects.filter(by_person=Person.objects.get(user=request.user))
        serializer = CarSerializers(queryset, many=True)
        return HttpResponse(JSONRenderer().render(serializer.data))

    def post(self, request, *args, **kwargs):
        serializer_class = CarSerializers(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            obj = Car.objects.create(by_person=Person.objects.get(user=request.user), **serializer_class.validated_data)

            return Response(status=status.HTTP_200_OK, data=obj.number)
        return Response(status=status.HTTP_200_OK, data="NO")

    def delete(self, request, *args, **kwargs):
        context = {"success": False}
        try:
            Car.objects.get(by_person__user=request.user, number=request.data['number']).delete()
            context["success"] = True
            return HttpResponse(json.dumps(context))
        except Exception as e:
            return HttpResponse(json.dumps(context))


class PickedOrderList(generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView):
    queryset = PickedOrder.objects.all()
    serializer_class = PickedOrderSerializers

    def get(self, request, *args, **kwargs):
        try:
            type = request.GET['id']
            if type == "1":  # get picked orders for driver
                context = {"success": False, "data": ''}
                print(str(Driver.objects.get(driver__user=request.user).pk))
                posts = PickedOrder.objects.filter(picked_by=Driver.objects.get(driver__user=request.user)).all()
                serializer = PickedOrderSerializers(posts, many=True)
                data1 = serializers.serialize("json", posts)
                context["data"] = serializer.data
                return HttpResponse(json.dumps(context))
            elif type == "2":  # get picked orders for a person
                posts = PickedOrder.objects.filter(order__order_by=Person.objects.get(user=request.user)).order_by(
                    'picked_time').all()
                details = {}
                all_posts = []
                i = 0
                for p in posts:
                    details['id'] = p.order.pk
                    details['title'] = p.order.post_title
                    details['description'] = p.order.description
                    details['deadline'] = p.order.deadline.ctime()
                    details['posted_time'] = p.order.order_time.ctime()
                    details['posts_picked_count'] = p.picked_by.count()
                    all_posts.append(details.copy())
                    i += 1
                return HttpResponse(json.dumps(all_posts))
            return HttpResponse("nothing")
        except Exception as ex:
            return HttpResponse("no -> " + str(ex))

    def post(self, request, *args, **kwargs):
        serializer_class = PickedOrderSerializers(data=request.data)
        context = {"success": False}
        try:
            if serializer_class.is_valid(raise_exception=True):
                pick = PickedOrder.objects.create(picked_by=Driver.objects.get(driver__user=request.user),
                                                  **serializer_class.validated_data)
                context["success"] = True
                dev = MobDevice.objects.get(user_id__user=request.user)
                person = Person.objects.get(user=request.user)

                body = {"user_id": request.user.pk,
                        "image": str(person.image), "full_name": request.user.first_name + " " + request.user.last_name,
                        "order_id": pick.order_id, "time": pick.picked_time,
                        "user_ssn": person.ssn, "user_email": request.user.email,
                        "user_number": person.phone_number}

                header = {"notif_type": "pick_order"}

                data = {"token": dev.device, "title": header, "body": body}
                notifications.send_notification(data)
                return HttpResponse(json.dumps(context))
            return HttpResponse(json.dumps(context))
        except Exception as ex:
            self.handle_exception(ex)

        def update(self, request, *args, **kwargs):
            context = {'success': True}

            return HttpResponse(json.dumps(context))

    def handle_exception(self, exc):
        context = {"success": False, 'exception': str(exc)}
        return HttpResponse(json.dumps(context))


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
    return HttpResponse(ser)
