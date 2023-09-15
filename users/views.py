
from rest_framework import viewsets
from users.models import User
from users.permissions import GetPermission, UpdatePermission
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [GetPermission | UpdatePermission]

