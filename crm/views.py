from rest_framework import viewsets

from .models import Car, Client, Repair, Part, Balance, Mechanic, SparePart, RepairSparePart, Service, RepairService
from .serializers import CarSerializer, ClientSerializer, RepairSerializer, PartSerializer, BalanceSerializer, MechanicSerializer, SparePartSerializer, RepairSparePartSerializer, ServiceSerializer, RepairServiceSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all().order_by('id')
    serializer_class = ClientSerializer

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all().order_by('id')
    serializer_class = CarSerializer

class MechanicViewSet(viewsets.ModelViewSet):
    queryset = Mechanic.objects.all().order_by('id')
    serializer_class = MechanicSerializer

class SparePartViewSet(viewsets.ModelViewSet):
    queryset = SparePart.objects.all().order_by('id')
    serializer_class = SparePartSerializer

class RepairSparePartViewSet(viewsets.ModelViewSet):
    queryset = RepairSparePart.objects.all().order_by('id')
    serializer_class = RepairSparePartSerializer

class RepairViewSet(viewsets.ModelViewSet):
    queryset = Repair.objects.all().order_by('id')
    serializer_class = RepairSerializer

class PartViewSet(viewsets.ModelViewSet):
    queryset = Part.objects.all().order_by('id')
    serializer_class = PartSerializer

class BalanceViewSet(viewsets.ModelViewSet):
    queryset = Balance.objects.all().order_by('id')
    serializer_class = BalanceSerializer

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all().order_by('id')
    serializer_class = ServiceSerializer

class RepairServiceViewSet(viewsets.ModelViewSet):
    queryset = RepairService.objects.all().order_by('id')
    serializer_class = RepairServiceSerializer
