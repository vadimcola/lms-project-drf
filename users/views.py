from rest_framework import viewsets
from users.models import User
from users.permissions import GetPermission, UpdatePermission
from users.serializers import UserSerializer, UsersSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    for user in queryset:
        if user.id:
            serializer_class = UserSerializer
        else:
            serializer_class = UsersSerializer
    permission_classes = [GetPermission | UpdatePermission]

