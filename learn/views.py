import stripe
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

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


class PaymentsCreate(generics.CreateAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    """Создание оплаты оп ID курса"""

    def perform_create(self, serializer):
        """Метод формирует ссылку для оплаты
        через сервис Stripe"""
        try:
            data = serializer.save(customer=self.request.user)
            name = data.paid_course
            unit_amount = data.paid_course.price
            stripe.api_key = settings.STRIPE_API_KEY
            product = stripe.Product.create(name=name)
            data_product = product.id
            amount = stripe.Price.create(
                unit_amount=int(unit_amount) * 100,
                currency="rub",
                product=data_product,
            )
            data_price = amount.id
            url_pay = stripe.checkout.Session.create(
                success_url="https://example.com/success",
                line_items=[
                    {
                        "price": data_price,
                        "quantity": 1,
                    },
                ],
                mode="payment"
            )
            data.customer = self.request.user
            data.payment_url = url_pay.url
            data.payment = int(amount.unit_amount_decimal) / 100
            data.payment_method = "card"
            data.payment_id = url_pay.id
            data.save()

        except stripe.error.StripeError as e:
            print(f"Error: {e}")
            return None


class PaymentCheckStatus(generics.RetrieveAPIView):
    """Проверка статуса оплаты"""
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer

    def get(self, request, pk):
        """Метод проверяет статус оплаты и добовляет в БД статус оплаты"""
        try:
            setting = get_object_or_404(Payments, id=pk)
            payment_id = str(setting.payment_id)
            stripe.api_key = settings.STRIPE_API_KEY
            data_pay = stripe.checkout.Session.retrieve(payment_id)
            payment_status = data_pay.payment_status
            if payment_status == "paid":
                setting.payment_status = True
                setting.save()
                return Response("Курс оплачен")
            else:
                return Response("Курс неоплачен")

        except stripe.error.StripeError as e:
            print(f"Error: {e}")
            return None


class PaymentDetail(generics.RetrieveAPIView):
    """ Детальный просмотр оплаты"""
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    permission_classes = (AllowAny,)


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
