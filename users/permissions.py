from rest_framework.permissions import BasePermission


class GetPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        elif request.method in ['GET']:
            return True
        else:
            return False


class UpdatePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        elif obj.pk == request.user.pk:
            if request.method in ['PUT', 'PATCH']:
                return True
        else:
            return False
