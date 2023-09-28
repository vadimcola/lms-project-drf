import stripe
from django_filters.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, permissions
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from learn.models import Course, Lesson, Payments, CourseSubscription
from learn.paginators import LessonPaginator, CoursePaginator
from learn.permissions import CustomPermission
from learn.serializers import CourseSerializer, PaymentsSerializer, LessonSerializer, CourseSubscriptionSerializer


class MixinQueryset:
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user.pk)
        return queryset


class CourseViewSet(MixinQueryset, viewsets.ModelViewSet):
    """CRUD Курса"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [CustomPermission]
    pagination_class = CoursePaginator

    def perform_create(self, serializer):
        """При создании курса его владелец, авторизованный пользователь"""
        new_course = serializer.save(owner=self.request.user)
        new_course.owner = self.request.user
        new_course.save()


class LessonList(MixinQueryset, generics.ListAPIView):
    """Просмотр списка уроков"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = LessonPaginator


class LessonDetail(MixinQueryset, generics.RetrieveAPIView):
    """Посмотр детальной информации выбранного урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonCreate(generics.CreateAPIView):
    """Создание урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [CustomPermission]

    def perform_create(self, serializer):
        """При создании урока его владелец, авторизованный пользователь """
        new_lesson = serializer.save(owner=self.request.user)
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonUpdate(MixinQueryset, generics.UpdateAPIView):
    """Обновоение урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDelete(generics.DestroyAPIView):
    """Удаление урока"""
    queryset = Lesson.objects.all()
    serializer_class = PaymentsSerializer
    permission_classes = [CustomPermission]


class PaymentsList(generics.ListAPIView):
    """Просмотр оплаты за Курс """
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['paid_course', 'paid_lesson', 'payment_method']
    ordering_fields = ['payment_date']
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        stripe.api_key = 'sk_test_51NutEgKP3JmokYuxFYXHCT1R788HpwldCZ2z7bhBUIrJuJkWozlppDYiJB3nqkPQxpg1l5YFX55sC4XO5O9Rva6200jQmRlwjr'
        product = stripe.Product.create(name=Payments.paid_course)
        data_product = product.id
        price = stripe.Price.create(
            unit_amount=1200000,
            currency="rub",
            product=data_product,
        )
        data_price = price.id
        url_pay = stripe.checkout.Session.create(
            success_url="https://example.com/success",
            line_items=[
                {
                    "price": data_price,
                    "quantity": 1,
                },
            ],
            mode="payment",
        )
        return Response(url_pay)





class CourseSubscriptionCreate(generics.CreateAPIView):
    """Подписка на курс"""
    queryset = CourseSubscription.objects.all()
    serializer_class = CourseSubscriptionSerializer

    def perform_create(self, serializer):
        new_subscription = serializer.save(user=self.request.user)
        new_subscription.user = self.request.user
        new_subscription.is_subscribed = True
        new_subscription.save()


class CourseSubscriptionDelete(generics.DestroyAPIView):
    """Удаление подписки на курс"""
    queryset = CourseSubscription.objects.all()
    serializer_class = CourseSubscriptionSerializer


class StripePaymentView(APIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        stripe.api_key = 'sk_test_51NutEgKP3JmokYuxFYXHCT1R788HpwldCZ2z7bhBUIrJuJkWozlppDYiJB3nqkPQxpg1l5YFX55sC4XO5O9Rva6200jQmRlwjr'
        try:
            amount = 100000  # Сумма платежа в копейках (в данном случае - 10 рублей)
            currency = 'rub'  # Валюта платежа (рубли)

            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                payment_method_types=['card']
            )

            return Response({'client_secret': intent.client_secret,
                             'created': intent.created,
                             'amount': intent.amount})

        except Exception as e:
            return Response({"error": str(e)})

