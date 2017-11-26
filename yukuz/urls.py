from django.conf.urls import url, include
from yukuz import views

urlpatterns = [
    # (?P<pk>\d+)/?
    url(r'^vtypelist/$', views.VehicleTypeList.as_view()),
    url(r'^car_view/$', views.CarView.as_view()),

    url(r'^post_update/$', views.update_post),
    url(r'^posts/$', views.PostsList.as_view()),
    url(r'^picked_orders/$', views.PickedOrderList.as_view()),

    url(r'^initialize/$', views.default_view),

    url(r'^get_price_class/$', view=views.getPriceClass),
    # url(r'^upload/$', views.UploadAvatar.as_view())
]
