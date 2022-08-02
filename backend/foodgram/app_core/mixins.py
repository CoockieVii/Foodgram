from app_users.models import Subscription


class AttributesForUser:
    def get_is_subscribed(self, obj):
        """Получение параметра is_subscribed."""
        user = self.context.get('request').user
        if Subscription.objects.filter(
                user=user,
                author=obj).exists():
            return True
        return False


class AttributesForSubscription(AttributesForUser):
    def get_recipes_count(self, obj):
        """Получение параметра recipes_count."""
        return Recipe.objects.filter(author__id=obj.id).count()

    def get_recipes(self, obj):
        """Получение параметра recipes_limit."""
        request = self.context.get('request')
        if request.GET.get('recipes_limit'):
            recipes_limit = int(request.GET.get('recipes_limit'))
            queryset = Recipe.objects.filter(author__id=obj.id).order_by('id')[
                       :recipes_limit]
        else:
            queryset = Recipe.objects.filter(author__id=obj.id).order_by('id')
        return RecipeMinifieldSerializer(queryset, many=True).data
