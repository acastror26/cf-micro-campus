from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, ResourceTypeViewSet, ResourceViewSet, ReservationViewSet, UserViewSet, LoginView

router = DefaultRouter()
router.register(r'rooms', RoomViewSet)
router.register(r'resource-types', ResourceTypeViewSet)
router.register(r'resources', ResourceViewSet)
router.register(r'reservations', ReservationViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('', include(router.urls)),
]