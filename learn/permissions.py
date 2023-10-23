from rest_framework.permissions import BasePermission


class CustomPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_superuser and not request.user.is_staff:
            return True
        elif request.user.is_superuser:
            return True
        elif request.method in ['GET', 'PUT', 'PATCH'] and request.user.is_staff:
            return True
        else:
            return False


