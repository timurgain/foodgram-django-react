from collections import namedtuple

from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES_NAME = namedtuple('ROLES_NAME', 'user admin')
ROLES = ROLES_NAME('user', 'admin')
ROLE_CHOICES = (
    ('user', ROLES.user),
    ('admin', ROLES.admin),
)


class User(AbstractUser):
    """Castom model user."""
    role = models.CharField(
        verbose_name='Роль пользователя',
        choices=ROLE_CHOICES,
        default=ROLES.user,
        max_length=max(len(role) for _, role in ROLE_CHOICES),
    )
    first_name = models.CharField(max_length=150, blank=True)

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def is_admin(self) -> bool:
        return self.role == ROLES.admin

    def __str__(self) -> str:
        return self.username[:30]


class Subscription(models.Model):
    """Table with subscriptions."""
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    following = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='following',
        verbose_name='Автор рецепта',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self) -> str:
        return f'{self.user} подписан на автора {self.author}'
