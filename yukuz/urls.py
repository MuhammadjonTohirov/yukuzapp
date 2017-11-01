from django.conf.urls import url, include
from yukuz import views

urlpatterns = [
    # (?P<pk>\d+)/?
    url(r'^personlist/$', views.PersonList.as_view()),
    url(r'^persondetails/(?P<pk>\d+)/?', views.PersonDetails.as_view()),
    url(r'^vtypelist/$', views.VehicleTypeList.as_view()),
    url(r'^get_user/$', views.get_id),

    url(r'^posts/$', views.PostsList.as_view()),
    url(r'^picked_orders/$', views.PickedOrderList.as_view()),
    url(r'^devices/$', views.CreateDevice.as_view()),
    url(r'^register/(?P<pk>[0-9]+)/$', views.RegisterView.as_view()),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^def/$', views.read_token),

    url(r'^get_price_class/$', view=views.getPriceClass),
    # url(r'^upload/$', views.UploadAvatar.as_view())
]
