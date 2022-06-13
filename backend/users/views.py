

from rest_framework.response import Response
from .models import User
from .serializers import FollowSerializer
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination


class CustomUserViewSet(UserViewSet):
    """Custom ViewSet based on Djoser ViewSet."""

    @action(methods=['get'], detail=False, url_path='subscriptions')
    def subscriptions(self, request, id=None):
        user = self.request.user
        following_people = User.objects.filter(following__user=user)
        serializer = FollowSerializer(
            following_people, context={'request': request}, many=True)
        return Response(serializer.data)

        # paginator = PageNumberPagination()
        # paginator.page_size = 5
        # result_page = paginator.paginate_queryset(following_people, request)
        # serializer = FollowSerializer(result_page, context={'request': request}, many=True)
        # return paginator.get_paginated_response(serializer.data)
