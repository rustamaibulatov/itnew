from django.db.models import Q

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

    def get_queryset(self):
        queryset = super().get_queryset()

        status = self.request.query_params.get('status')
        mechanic = self.request.query_params.get('mechanic')
        car = self.request.query_params.get('car')
        search = self.request.query_params.get('search')
        ordering = self.request.query_params.get('ordering')

        if status:
            queryset = queryset.filter(status=status)

        if mechanic:
            queryset = queryset.filter(mechanic_id=mechanic)

        if car:
            queryset = queryset.filter(car_id=car)

        if search:
            queryset = queryset.filter(
                Q(description__icontains=search) |
                Q(car__license_plate__icontains=search) |
                Q(car__vin__icontains=search) |
                Q(car__client__full_name__icontains=search) |
                Q(car__client__phone__icontains=search)
            )

        allowed_ordering = [
            'id',
            '-id',
            'created_at',
            '-created_at',
            'work_cost',
            '-work_cost',
        ]

        if ordering in allowed_ordering:
            queryset = queryset.order_by(ordering)

        return queryset

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
