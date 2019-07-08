from photos.api.views import PhotoViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', PhotoViewSet, basename='photos')
urlpatterns = router.urls