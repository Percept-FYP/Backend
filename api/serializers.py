from rest_framework import serializers
from .models import attendance, info, teacher, Class, attendance, Student, Subject
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["usn"]


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['subject_code']


class AttendanceSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)

    class Meta:
        model = attendance
        fields = ["student", 'attend', 'time']


class ClassSerializer(serializers.ModelSerializer):
    attendance_set = AttendanceSerializer(many=True)
    subject = SubjectSerializer()

    class Meta:
        model = Class
        fields = ['subject', "id", 'attendance_set']

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

####################


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['role'] = user.role
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
