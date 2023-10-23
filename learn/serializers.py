from rest_framework import serializers

from learn.models import Course, Lesson, Payments


class LessonSerializer(serializers.ModelSerializer):
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
