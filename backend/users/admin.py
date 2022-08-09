from django.contrib import admin

from .models import User, Subscription


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'password']
    actions_on_bottom = True
    search_fields = ['username', 'email']
    empty_value_display = '-пусто-'


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'author', 'created']
    actions_on_bottom = True
    search_fields = ['user', 'author']
    empty_value_display = '-пусто-'
