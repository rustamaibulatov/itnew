from rest_framework.routers import DefaultRouter

from .views import CarViewSet, ClientViewSet, RepairViewSet, PartViewSet, BalanceViewSet

router = DefaultRouter()
router.register('clients', ClientViewSet)
router.register('cars', CarViewSet)
router.register('repairs', RepairViewSet)
router.register('parts', PartViewSet)
router.register('balances', BalanceViewSet)

urlpatterns = router.urls
