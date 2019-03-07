from django.conf.urls import url, include
from yukuz_firebase import views

urlpatterns = [
    url(r'^devices/$', views.CreateDevice.as_view()),
]
