from django.shortcuts import get_list_or_404
from djoser.serializers import SetPasswordSerializer
from rest_framework import viewsets, status, permissions, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action

from core.validaters import validate_subscription
from .models import User, Subscription
from .serializers import CreateUserSerializer
from .serializers import SubscriptionSerializer
from .serializers import UserSerializer


class CreateListRetrieveViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    pass


class UserViewSet(CreateListRetrieveViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_permissions(self):
        if self.action in ('create', 'list'):
            return [permissions.AllowAny()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        if self.action == 'set_password':
            return SetPasswordSerializer
        if self.action in ('subscribe', 'subscriptions'):
            return SubscriptionSerializer
        return UserSerializer

    @action(detail=False)
    def me(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(methods=('POST',), detail=False)
    def set_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.request.user.set_password(
            serializer.validated_data['new_password'])
        self.request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return get_list_or_404(User, subscriber__user=self.request.user)

    def create(self, request, *args, **kwargs):
        author_id = self.kwargs['users_id']
        author = get_object_or_404(User, id=author_id)
        validate = validate_subscription(author, request.user)
        if validate:
            return Response(data=validate['errors'], status=validate['status'])
        if Subscription.objects.create(user=request.user, author=author):
            serializer = self.get_serializer(request.user)
            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        author_id = self.kwargs['users_id']
        user_id = request.user.id
        if get_object_or_404(
                Subscription,
                user__id=user_id,
                author__id=author_id).delete():
            return Response(status=status.HTTP_204_NO_CONTENT)
