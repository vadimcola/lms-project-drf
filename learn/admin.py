from django.contrib import admin

from learn.models import Course, Lesson, Payments, CourseSubscription


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('pk', 'course_name', 'course_preview', 'course_comment')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('pk', 'lesson_name', 'course_name')


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'customer', 'payment')


@admin.register(CourseSubscription)
class CourseSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'course', 'is_subscribed')
