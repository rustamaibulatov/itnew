from rest_framework import viewsets

from .models import Car, Client
from .serializers import CarSerializer, ClientSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all().order_by('id')
    serializer_class = ClientSerializer

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all().order_by('id')
    serializer_class = CarSerializer
