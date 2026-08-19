from rest_framework.routers import DefaultRouter

from .views import CarViewSet, ClientViewSet, RepairViewSet, PartViewSet, BalanceViewSet, MechanicViewSet, SparePartViewSet, RepairSparePartViewSet

router = DefaultRouter()
router.register('clients', ClientViewSet)
router.register('cars', CarViewSet)
router.register('mechanics', MechanicViewSet)
router.register('spare-parts', SparePartViewSet)
router.register('repair-spare-parts', RepairSparePartViewSet)
router.register('repairs', RepairViewSet)
router.register('parts', PartViewSet)
router.register('balances', BalanceViewSet)

urlpatterns = router.urls
