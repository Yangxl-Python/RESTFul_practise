from rest_framework import serializers
from rest_framework import exceptions

from student.models import Student


class StudentModelSerializer(serializers.Serializer):
    name = serializers.CharField()
    gender = serializers.SerializerMethodField()
    grade = serializers.SerializerMethodField()

    def get_gender(self, obj):
        return obj.get_gender_display()

    def get_grade(self, obj):
        return obj.get_grade_display()


class StudentModelDeserializer(serializers.Serializer):
    name = serializers.CharField(max_length=30,
                                 min_length=1,
                                 error_messages={
                                     'max_length': '长度不能大于10',
                                     'min_length': '长度不能小于6',
                                 })
    gender = serializers.IntegerField()
    grade = serializers.IntegerField()

    def validate_name(self, attrs):
        if '1' in attrs:
            raise exceptions.ValidationError('用户名异常')
        return attrs

    def validate(self, attrs):
        if attrs.get('gender') in (0, 1, 2) and attrs.get('grade') in range(0, 5):
            return attrs
        raise exceptions.ValidationError('数据超出范围')

    def create(self, validated_data):
        return Student.objects.create(**validated_data)
