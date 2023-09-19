from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from learn.models import Course, Lesson, Payments, CourseSubscription
from learn.permissions import CustomPermission
from learn.serializers import CourseSerializer, PaymentsSerializer, LessonSerializer, CourseSubscriptionSerializer


class MixinQueryset:
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user.pk)
        return queryset


class CourseViewSet(MixinQueryset, viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [CustomPermission]

    def perform_create(self, serializer):
        new_course = serializer.save(owner=self.request.user)
        new_course.owner = self.request.user
        new_course.save()


class LessonList(MixinQueryset, generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDetail(MixinQueryset, generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonCreate(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [CustomPermission]

    def perform_create(self, serializer):
        new_lesson = serializer.save(owner=self.request.user)
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonUpdate(MixinQueryset, generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDelete(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = PaymentsSerializer
    permission_classes = [CustomPermission]


class PaymentsList(generics.ListAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['paid_course', 'paid_lesson', 'payment_method']
    ordering_fields = ['payment_date']


class CourseSubscriptionCreate(generics.CreateAPIView):
    queryset = CourseSubscription.objects.all()
    serializer_class = CourseSubscriptionSerializer

    def perform_create(self, serializer):
        new_subscription = serializer.save(user=self.request.user)
        new_subscription.user = self.request.user
        new_subscription.is_subscribed = True
        new_subscription.save()
        return Response({'message': 'Вы успешно подписались на курс.'})

