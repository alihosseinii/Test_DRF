from rest_framework.response import Response
from rest_framework import viewsets, status, generics, permissions, serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import UserInformation, Reservation, IdentityInformation
from .serializer import UserLoginSerializer, ReservationSerializer, SingupSerializer, UserInfoSerializer
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from train.models import ExistTrains
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
    permission_classes = [IsAuthenticated]
    queryset = Reservation.objects.all()

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user).select_related('train')

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
        return obj


    def perform_create(self, serializer):

        reservation: Reservation = serializer.save(user=self.request.user)
        train: ExistTrains = reservation.train
        if hasattr(train, 'capacity'):
            train.capacity = train.capacity - reservation.quantity
            train.save()
        serializer.save(user=self.request.user)


    def perform_destroy(self, instance: Reservation):
        train = instance.train
        if hasattr(train, 'capacity'):
            train.capacity = train.capacity + instance.quantity
            train.save()
        instance.delete()
   

class ShowInfo(viewsets.ModelViewSet):
    serializer_class = UserInfoSerializer
    permission_classes = [IsAuthenticated]
    queryset = IdentityInformation.objects.all()

    def get_queryset(self):
        return IdentityInformation.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
