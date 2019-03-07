from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.utils import json

from yukuz_firebase.models import MobDevice
from yukuz_firebase.serializers import DevSerializer

from yukuz_firebase.models import Person


class CreateDevice(generics.ListAPIView, generics.CreateAPIView):
    queryset = MobDevice.objects.all()
    serializer_class = DevSerializer

    def get(self, request, *args, **kwargs):
        # header = request.META['HTTP_AUTHORIZATION']
        q = MobDevice.objects.all()
        ser = DevSerializer(q, many=True)
        return Response(ser.data)

        # @api_view(['POST', 'GET'])

    # def perform_create(self, serializer):
    #     serializer.save(device=self.request.data['device'], user_id=Person.objects.get(user=self.request.user),
    #                     is_driver=self.request.data['is_driver'], dev_version=self.request.data['dev_version'])
    def post(self, request, *args, **kwargs):
        serializers = DevSerializer(data=request.data)
        context = {'created': False}
        person = Person.objects.filter(user=request.user)
        if person.count() > 0:
            if serializers.is_valid(True):
                MobDevice.objects.create(user_id=Person.objects.get(user=request.user), **serializers.validated_data)
                context = {'created': True}
                return Response(status=status.HTTP_200_OK, data=json.dumps(context))
            return Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps(context))

        context['message'] = 'Account not full'
        response = Response(status=status.HTTP_404_NOT_FOUND, data=context)
        print(response.status_text)
        return response
