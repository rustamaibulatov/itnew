from django.shortcuts import render
from django.db.models import Q

from rest_framework import viewsets, serializers

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
    def perform_destroy(self, instance):
        if instance.repair.status == 'completed':
            raise serializers.ValidationError({
            'repair': 'Нельзя удалять запчасти из завершённого ремонта.'
        })

        spare_part = instance.spare_part
        spare_part.stock_quantity += instance.quantity
        spare_part.save(update_fields=['stock_quantity'])

        instance.delete()

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

    def perform_destroy(self, instance):
        if instance.repair.status == 'completed':
            raise serializers.ValidationError({
                'repair': 'Нельзя удалять услуги из завершённого ремонта.'
            })

        instance.delete()

def dashboard_view(request):
    clients_count = Client.objects.count()
    cars_count = Car.objects.count()

    active_repairs_count = Repair.objects.filter(
        status='in_progress'
    ).count()

    completed_repairs = Repair.objects.filter(
        status='completed'
    ).prefetch_related(
        'repair_services',
        'spare_parts'
    )

    total_profit = 0

    for repair in completed_repairs:
        services_total = sum(
            item.price for item in repair.repair_services.all()
        )

        parts_total = sum(
            item.sale_price for item in repair.spare_parts.all()
        )

        parts_cost = sum(
            item.purchase_price for item in repair.spare_parts.all()
        )

        total_profit += services_total + parts_total - parts_cost

    recent_repairs = Repair.objects.select_related(
        'car'
    ).prefetch_related(
        'repair_services',
        'spare_parts'
    ).order_by('-created_at')[:5]

    for repair in recent_repairs:
        services_total = sum(
            item.price for item in repair.repair_services.all()
        )

        parts_total = sum(
            item.sale_price for item in repair.spare_parts.all()
        )

        repair.total = services_total + parts_total

    context = {
        'clients_count': clients_count,
        'cars_count': cars_count,
        'active_repairs_count': active_repairs_count,
        'total_profit': total_profit,
        'recent_repairs': recent_repairs,
    }

    return render(
        request,
        'dashboard.html',
        context
    )
