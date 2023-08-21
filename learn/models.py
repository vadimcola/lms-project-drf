from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    course_name = models.CharField(max_length=255, **NULLABLE,
                                   verbose_name='Наименование курса')
    course_preview = models.ImageField(**NULLABLE, verbose_name='Картинка', )
    course_comment = models.TextField(**NULLABLE, verbose_name='Описание')

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
    course_name = models.ForeignKey('Course', on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.lesson_name}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
