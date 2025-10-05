from rest_framework.response import Response
from rest_framework import viewsets, status, generics, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import UserInformation, Reservation, IdentityInformation
from .serializer import UserLoginSerializer, ReservationSerializer, SingupSerializer, UserInfoSerializer
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
User = get_user_model()

class SingupView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SingupSerializer

    def post(self, request):
        serializer = SingupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "user registered successfully"}, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data["phone_number"]
        password = serializer.validated_data["password"]

        try:
            user = UserInformation.objects.get(phone_number=phone)
        except UserInformation.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })


class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Reservation.objects.all()

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()

    @action(detail=False, methods=['get'])
    def my_tickets(self, request):
        reservations = self.get_queryset()
        serializer = self.get_serializer(reservations, many=True)
        return Response(serializer.data)


class ShowInfo(viewsets.ModelViewSet):
    serializer_class = UserInfoSerializer
    permission_classes = [IsAuthenticated]
    queryset = IdentityInformation.objects.all()
    def get_queryset(self):
        return IdentityInformation.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
