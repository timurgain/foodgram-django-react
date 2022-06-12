from rest_framework import filters, permissions, viewsets, mixins

from .models import Subscription
from .serializers import SubscriptionSerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    """ViewSet for model Subscription."""
    serializer_class = SubscriptionSerializer
    # permission_classes = (IsUserOrForbidden,)
    filter_backends = (
        filters.SearchFilter,
    )

    # Поиск по '(ForeignKey текущей модели)__(имя поля в связанной модели)'
    search_fields = ('=following_id__username',)

    def get_queryset(self):
        user = self.request.user
        return Subscription.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DoSubscribeViewSet(mixins.CreateModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    """."""
    serializer_class = SubscriptionSerializer
