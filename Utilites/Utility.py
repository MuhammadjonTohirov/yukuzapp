from rest_framework import status
from rest_framework.response import Response
from django.utils.encoding import force_text
from rest_framework import serializers, status
from rest_framework.exceptions import APIException, ErrorDetail
from django.utils.translation import ugettext_lazy as _
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict


class YResponse:
    context = {
        'status': False
    }

    @staticmethod
    def failure_response(error_message):
        YResponse.context['result'] = error_message
        YResponse.context['status'] = status.HTTP_400_BAD_REQUEST
        return Response(data=error_message, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def success_response(message):
        YResponse.context['status'] = status.HTTP_200_OK
        YResponse.context['result'] = message
        return Response(data=message, status=status.HTTP_200_OK)

    @staticmethod
    def created_response(json_message):
        YResponse.context['status'] = status.HTTP_201_CREATED
        return Response(json_message, status=status.HTTP_201_CREATED)

    @staticmethod
    def reserved_response(json_message):
        YResponse.context['status'] = status.HTTP_306_RESERVED
        YResponse.context['result'] = json_message
        return Response(json_message, status=status.HTTP_306_RESERVED)


class ValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Invalid input.')
    default_code = 'invalid'

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        # For validation failures, we may collect many errors together,
        # so the details should always be coerced to a list if not already.
        self.detail = _get_error_details(detail, code)


def _get_error_details(data, default_code=None):
    return _get_result_detail(data, False)


def _get_success_details(data, default_code=None):
    return _get_result_detail(data, True)


def _get_result_detail(data, status):
    return {
        'status': status,
        'detail': data
    }
