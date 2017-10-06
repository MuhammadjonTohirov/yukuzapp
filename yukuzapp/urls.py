"""yukuzapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib.auth.models import User
from django.contrib import admin
from yukuz.resources import UserList
from tastypie.api import Api
from rest_framework.authtoken import views
from yukuz.resources import VehicleTypeList, VehiclesList, PostOrderList, PickedOrderList, UserAuthResource, DriverList
from rest_framework import routers, serializers, viewsets

yukuz_app_api = Api(api_name='yukuz')
yukuz_app_api.register(UserList())
yukuz_app_api.register(VehicleTypeList())
yukuz_app_api.register(PostOrderList())
yukuz_app_api.register(PickedOrderList())
yukuz_app_api.register(UserAuthResource())
yukuz_app_api.register(DriverList())
yukuz_app_api.register(VehiclesList())

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(yukuz_app_api.urls)),
    url(r'^rest/', include('yukuz.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', include('rest_framework_docs.urls')),
    url(r'^api-gettoken/$', views.obtain_auth_token),
    url(r'^auth/', include('rest_framework_social_oauth2.urls'))
]
