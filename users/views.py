from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, status, generics
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import UserInformation, Reservation, IdentityInformation
from .serializer import UserInfoSerializer, ReservationSerializer, loginserializer, singupserializer

class login(APIView):
    permission_classes = [AllowAny,]

    def post(self, request):
        serializer = loginserializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),    
        }, status= status.HTTP_200_OK)
    

class singup(generics.CreateAPIView):
    serializer_class = singupserializer
    permission_classes = [AllowAny,]


class reservation(generics.CreateAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated,]


class ShowTickets(viewsets.ReadOnlyModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

class ShowInfo(viewsets.ModelViewSet):
    queryset = IdentityInformation.objects.all()
    serializer_class = UserInformation