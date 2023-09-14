
from rest_framework import viewsets
from users.models import User
from users.permissions import GetPermission, UpdatePermission
from users.serializers import UserSerializer, UsersSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    serializer_class = UsersSerializer
    permission_classes = [GetPermission | UpdatePermission]

