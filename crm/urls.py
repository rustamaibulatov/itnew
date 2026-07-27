from rest_framework.routers import DefaultRouter

from .views import CarViewSet, ClientViewSet

router = DefaultRouter()
router.register('clients', ClientViewSet)
router.register('cars', CarViewSet)

urlpatterns = router.urls
