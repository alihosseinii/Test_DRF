from django.urls import path , include
from rest_framework.routers import DefaultRouter
from .views import singup, login, ShowInfo, reservation, ShowTickets

router = DefaultRouter()
router.register("", ShowInfo)

router2 = DefaultRouter()
router2.register('', ShowTickets)

urlpatterns = [
    path('singup/', singup.as_view, name="apisingup"),
    path('login/', login.as_view, name="apilogin"),
    path('information/', include(router.urls)),
    path('reserve/', reservation.as_view, name='apireserve'),
    path('tickets/', include(router2.urls)),
]