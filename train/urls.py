from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShowTrainList, ShowCity

router = DefaultRouter()
router.register("", ShowTrainList)

router2 = DefaultRouter()
router2.register("", ShowCity)

# router3 = DefaultRouter()
# router3.register("order/", )

urlpatterns = [
     path("trains/", include(router.urls)),
     path("city/", include(router2.urls)),
]