from django.conf.urls import url, include
from mfirebase import views

urlpatterns = [
    url(r'^devices/$', views.CreateDevice.as_view()),
]
