from django.shortcuts import render
from rest_framework import viewsets
from .models import ExistTrains, City
from .serializer import TrainSerializer, CitySerializer, TrainDetailSerializer
from .filters import filter_trains
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

class ShowTrainList(viewsets.ReadOnlyModelViewSet):
    queryset = ExistTrains.objects.order_by("depratortime").all()
    filterset_class = filter_trains
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_feilds = ['origin', 'price', 'depratortime',]
    def get_serializer_class(self):
        if self.action == "list":
            return TrainSerializer
        elif self.action == "retrieve":
            return TrainDetailSerializer
        return TrainSerializer

class ShowCity(viewsets.ReadOnlyModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer