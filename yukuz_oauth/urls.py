from django.conf.urls import url

from yukuz_oauth import views

urlpatterns = [
    url(r'^person_list/$', views.PersonList.as_view()),
    url(r'^person_details/(?P<pk>\d+)/?', views.PersonView.as_view()),
    url(r'^person_detail/$', views.PersonView.as_view()),
    url(r'^person_update/(?P<pk>\d+)/?', views.PersonView.as_view()),
    url(r'^get_user/$', views.get_id),
    url(r'^driver_create/$', views.DriverView.as_view()),

    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    #
    url(r'^register/(?P<pk>[0-9]+)/$', views.RegisterAndUpdateView.as_view()),
    url(r'^register/$', views.RegisterAndUpdateView.as_view()),
    url(r'^login/$', views.obtain_auth_token),

]
