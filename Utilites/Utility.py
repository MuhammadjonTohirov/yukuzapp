from rest_framework import status
from rest_framework.response import Response


class YResponse():
    context = {
        'status': False
    }

    @staticmethod
    def failure_response(error_message):
        YResponse.context['detail'] = error_message
        YResponse.context['status'] = False
        return Response(data=YResponse.context, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def success_response(message):
        YResponse.context['status'] = True
        YResponse.context['detail'] = message
        return Response(data=YResponse.context, status=status.HTTP_200_OK)

    @staticmethod
    def created_response(json_message):
        YResponse.context['status'] = True
        return Response(json_message, status=status.HTTP_201_CREATED)

    @staticmethod
    def reserved_response(json_message):
        YResponse.context['status'] = False
        YResponse.context['detail'] = json_message
        return Response(YResponse.context, status=status.HTTP_306_RESERVED)
