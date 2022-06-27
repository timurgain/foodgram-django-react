from django.urls import include, path, re_path

from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet

app_name = 'users'

router_v1 = DefaultRouter()
router_v1.register(prefix=r'users', viewset=CustomUserViewSet)

urlpatterns = [
    path('', include(router_v1.urls)),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
