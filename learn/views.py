from rest_framework import viewsets

from learn.models import Course
from learn.serializers import CourseSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
