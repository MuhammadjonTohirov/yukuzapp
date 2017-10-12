from django.conf.urls import url, include
from yukuz import views

urlpatterns = [
    url(r'^userlist/$', views.PersonList.as_view()),
    url(r'^vtypelist/$', views.VehicleTypeList.as_view()),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^register/$', views.RegisterView.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^def/$', views.default_view)
]
