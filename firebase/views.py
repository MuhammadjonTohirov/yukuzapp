from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.response import Response

from firebase.models import MobDevice
from firebase.serialisers import DevSerializer


class CreateDevice(generics.ListAPIView, generics.CreateAPIView):
    queryset = MobDevice.objects.all()
    serializer_class = DevSerializer

    def get(self, request, *args, **kwargs):
        # header = request.META['HTTP_AUTHORIZATION']
        q = MobDevice.objects.all()
        ser = DevSerializer(q, many=True)
        return Response(ser.data)

        # @api_view(['POST', 'GET'])
