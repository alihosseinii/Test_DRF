from django.urls import path , include
from rest_framework.routers import DefaultRouter
from .views import SingupView, LoginView, ShowInfo, ReservationViewSet



router = DefaultRouter()
router.register('', ReservationViewSet)

router2 = DefaultRouter()
router2.register('', ShowInfo)

urlpatterns = [
    path('singup/', SingupView.as_view(), name="singup"),
    path('login/', LoginView.as_view(), name="login"),
    path('information/', include(router2.urls), name='information'),
    path('tickets/', include(router.urls), name="tickets"),
]