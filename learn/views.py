from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny

from learn.models import Course, Lesson, Payments
from learn.permissions import CoursePermission, LessonPermission
from learn.serializers import CourseSerializer, PaymentsSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, CoursePermission]

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user.pk)
        return queryset

    def perform_create(self, serializer):
        new_course = serializer.save(owner=self.request.user)
        new_course.owner = self.request.user
        new_course.save()


class LessonList(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, LessonPermission]

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user.pk)
        return queryset


class LessonDetail(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [AllowAny, LessonPermission]


class LessonCreate(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [AllowAny, LessonPermission]

    def perform_create(self, serializer):
        new_lesson = serializer.save(owner=self.request.user)
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonUpdate(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, LessonPermission]


class LessonDelete(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = PaymentsSerializer
    permission_classes = [AllowAny, LessonPermission]


class PaymentsList(generics.ListAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['paid_course', 'paid_lesson', 'payment_method']
    ordering_fields = ['payment_date']
    permission_classes = [IsAuthenticated]
