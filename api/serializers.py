from rest_framework import serializers
from .models import attendance, info, teacher, Class, attendance, Student


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class AttendanceSerializer(serializers.ModelSerializer):
    teacher = StudentSerializer(many=True, read_only=True)

    class Meta:
        model = attendance
        fields = ['attend', 'time', 'Class']

    def create(self, validated_data):
        class_data = validated_data.pop('tracks')
        attendance = attendance.objects.create(**validated_data)
        for class_data in class_data:
            Class.objects.create(attendance=attendance, **class_data)
        return attendance


class infoSerializer(serializers.ModelSerializer):
    class Meta:
        model = info
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = teacher
        fields = ['name']


class ClassSerializer(serializers.ModelSerializer):

    class Meta:
        model = Class
        fields = ['teacher','subject','class_id','image']
