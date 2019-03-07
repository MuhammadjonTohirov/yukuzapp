from django.conf.urls import url, include
from yukuz_main import views

urlpatterns = [
    # (?P<pk>\d+)/?
    url(r'^vehicle_type_list/$', views.VehicleTypeList.as_view()),
    url(r'^car_view/$', views.CarView.as_view()),

    url(r'^post_update/$', views.update_post),
    url(r'^posts/$', views.PostsList.as_view()),
    url(r'^picked_orders/$', views.PickedOrderList.as_view()),

    url(r'^initialize/$', views.default_view),

    url(r'^get_currency_types/$', view=views.get_currency_types),
    # url(r'^upload/$', views.UploadAvatar.as_view())
]
