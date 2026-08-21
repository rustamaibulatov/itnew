from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import CarViewSet, ClientViewSet, RepairViewSet, PartViewSet, BalanceViewSet, MechanicViewSet, SparePartViewSet, RepairSparePartViewSet, ServiceViewSet, RepairServiceViewSet, dashboard_view

router = DefaultRouter()
router.register('clients', ClientViewSet)
router.register('cars', CarViewSet)
router.register('mechanics', MechanicViewSet)
router.register('spare-parts', SparePartViewSet)
router.register('repair-spare-parts', RepairSparePartViewSet)
router.register('repairs', RepairViewSet)
router.register('parts', PartViewSet)
router.register('balances', BalanceViewSet)
router.register('services', ServiceViewSet)
router.register('repair-services', RepairServiceViewSet)

urlpatterns = router.urls + [
    path('dashboard/', dashboard_view, name='dashboard'),
]



