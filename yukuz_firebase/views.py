from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json
from Utilites.Utility import YResponse
from yukuz_firebase.models import MobDevice
from yukuz_firebase.serializers import DevSerializer

from yukuz_firebase.models import Person


class CreateDevice(generics.ListAPIView, generics.CreateAPIView):
    queryset = MobDevice.objects.all()
    serializer_class = DevSerializer

    def get(self, request, *args, **kwargs):
        q = MobDevice.objects.all()
        ser = DevSerializer(q, many=True)
        return Response(ser.data)

    def post(self, request, *args, **kwargs):
        serializers = DevSerializer(data=request.data)
        context = {'created': False}
        person = Person.objects.filter(user=request.user)
        if person.count() > 0:
            if serializers.is_valid(True):
                obj = MobDevice.objects.create(user_id=Person.objects.get(user=request.user), **serializers.validated_data)
                context = {'instance': obj.dict(),
                           'message': 'The device has been added successfully'}
                return YResponse.success_response(context)
            return YResponse.failure_response(context)

        context['message'] = 'Account not full'
        response = YResponse.failure_response(context)
        print(response.status_text)
        return response
