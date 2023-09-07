from django.conf import settings
from django.db import models
from django.utils import timezone

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    course_name = models.CharField(max_length=255, **NULLABLE,
                                   verbose_name='Наименование курса')
    course_preview = models.ImageField(**NULLABLE, verbose_name='Картинка', )
    course_comment = models.TextField(**NULLABLE, verbose_name='Описание')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE,
                              verbose_name='Владелец')

    def __str__(self):
        return f'{self.course_name}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    lesson_name = models.CharField(max_length=255, **NULLABLE,
                                   verbose_name='Наименование урока')
    lesson_preview = models.ImageField(**NULLABLE, verbose_name='Картинка', )
    lesson_comment = models.TextField(**NULLABLE, verbose_name='Описание')
    lesson_url = models.URLField(max_length=200, **NULLABLE, verbose_name='Ссылка')
    course_name = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE,
                                    related_name='course')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE,
                              verbose_name='Владелец')

    def __str__(self):
        return f'{self.lesson_name}, {self.course_name}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Payments(models.Model):
    PAY = [
        ('cash', 'Наличные'),
        ('account', 'Оплата на счет')
    ]

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE,
                                 related_name='customer', verbose_name='Пользователь')
    payment_date = models.DateField(default=timezone.now, verbose_name='Дата оплаты')
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE,
                                    verbose_name='Оплаченный курс')
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, **NULLABLE,
                                    verbose_name='Оплаченный урок')
    payment = models.IntegerField(verbose_name='Сумма оплаты')
    payment_method = models.CharField(max_length=7, choices=PAY,
                                      verbose_name='Метод оплаты')

    def __str__(self):
        return f'{self.customer}'

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'
