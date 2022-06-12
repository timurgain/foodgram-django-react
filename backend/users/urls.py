from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from .views import SubscriptionViewSet, DoSubscribeViewSet

app_name = 'users'

router = DefaultRouter()
router.register(
    prefix='subscriptions',
    viewset=SubscriptionViewSet,
    basename='subscriptions',
)
router.register(
    prefix=r'(?P<user_id>\d+)/subscribe/',
    viewset=DoSubscribeViewSet,
    basename='subscribe',
)

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include(router.urls)),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
