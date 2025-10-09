from django.urls import path , include
from rest_framework.routers import DefaultRouter
from .views import SingupView, LoginView, ShowInfo, ReservationViewSet



router = DefaultRouter()
router.register(r'tickets', ReservationViewSet)
router.register(r'information', ShowInfo)

urlpatterns = [
    path('singup/', SingupView.as_view(), name="singup"),
    path('login/', LoginView.as_view(), name="login"),
] + router.urls