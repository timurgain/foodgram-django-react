from django.contrib import admin

from .models import Follow, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'date_joined')
    list_filter = ('username', 'email',)
    search_fields = ('username', 'email',)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('following', 'user',)
