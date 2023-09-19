from rest_framework import serializers

from learn.models import Course, Lesson, Payments, CourseSubscription
from learn.validators import validate_url


class LessonSerializer(serializers.ModelSerializer):
    lesson_url = serializers.URLField(validators=[validate_url])

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    count_lesson = serializers.IntegerField(source='course.all.count', read_only=True)
    lesson = LessonSerializer(source='course', many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['course_name', 'course_preview', 'course_comment', 'count_lesson', 'lesson']


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'


class CourseSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSubscription
        fields = '__all__'
