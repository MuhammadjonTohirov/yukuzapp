from django.conf import settings
from pyfcm import FCMNotification


# d1UDLdQvf64:APA91bFPmHDNVNZJeoUkxPvIzdtYJe5X5QInKGp6ht7EvQtcIN3T8N23YlgpGk232lePrRiYt1jIhNuqMRJLb7mY8VMSButM5CUinDZrGHrqQ-QhXYbaEBwHBb-RiQVMUglUhrmLzWYi
def send_notification(data):
    try:
        push_service = FCMNotification(api_key=settings.FCM_APIKEY)
        reg_id = data['token']
        title = data['title']
        body = data['body']
        result = push_service.notify_single_device(registration_id=reg_id, message_title=title, message_body=body)
        return result
    except Exception as e:
        return e


def send_notifications(data):
    """:returns(result of push_service.notify_multiple_devices function)"""
    try:
        push_service = FCMNotification(api_key=settings.FCM_APIKEY)
        reg_ids = data['tokens']
        title = data['title']
        body = data['body']
        result = push_service.notify_multiple_devices(registration_ids=reg_ids, message_title=title, message_body=body)
        return result
    except Exception as e:
        return e
