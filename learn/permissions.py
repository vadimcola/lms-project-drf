from rest_framework.permissions import BasePermission


class LessonPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'PUT', 'PATCH'] and request.user.is_staff:
            return True
        else:
            return False


class CoursePermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'PUT', 'PATCH'] and request.user.is_staff:
            return True
        else:
            return False


