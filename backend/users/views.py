from django.shortcuts import get_object_or_404

from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Follow, User
from .serializers import CustomDjoserUserSerializer, PostFollowSerializer


class CustomUserViewSet(UserViewSet):
    """Custom ViewSet based on Djoser ViewSet."""

    @action(methods=['get'], detail=False,
            permission_classes=[permissions.IsAuthenticated])
    def subscriptions(self, request):
        user = self.request.user
        following_people = User.objects.filter(following__user=user)
        paginator = PageNumberPagination()
        paginator.page_size = 5
        result = paginator.paginate_queryset(queryset=following_people,
                                             request=request)
        serializer = CustomDjoserUserSerializer(
            result, context={'request': request}, many=True)
        return paginator.get_paginated_response(serializer.data)

    @action(methods=['post'], detail=True,
            permission_classes=[permissions.IsAuthenticated])
    def subscribe(self, request, id=None):
        user = self.request.user
        following = get_object_or_404(User, id=id)
        serializer = PostFollowSerializer(
            data={'user': user.id, 'following': following.id},
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)

        Follow.objects.create(user=user, following=following)
        serializer = CustomDjoserUserSerializer(
            following, context={'request': request})
        return Response(data=serializer.data,
                        status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def subscribe_delete(self, request, id=None):
        user = self.request.user
        following = get_object_or_404(User, id=id)
        follow_entry = (Follow.objects
                        .filter(user=user, following=following))
        if not follow_entry.exists():
            return Response('There was no such subscription.',
                            status=status.HTTP_400_BAD_REQUEST)
        follow_entry.delete()
        return Response('Successful unsubscribe.',
                        status=status.HTTP_204_NO_CONTENT)
