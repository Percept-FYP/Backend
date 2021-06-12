from rest_framework import serializers
from .models import attendance, info, teacher, Class, attendance, Student, Subject


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["usn"]


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['subject_code']


class AttendanceSerializer(serializers.ModelSerializer):
    student = StudentSerializer()

    class Meta:
        model = attendance
        fields = ["student", 'attend', 'time']


class ClassSerializer(serializers.ModelSerializer):
    attendance_set = AttendanceSerializer(many=True)


    class Meta:
        model = Class
        fields = ['subject', "id", 'attendance_set']

    def create(self, validated_data):
            attendances_data = validated_data.pop('attendance_set')
            print("thi s",attendances_data)
            ClASS = Class.objects.create(**validated_data)
            for attendance_data in attendances_data:
                print("thi s",attendance_data)
                attendance.objects.create(Class=ClASS, **attendance_data)
            return Class       



class infoSerializer(serializers.ModelSerializer):
    class Meta:
        model = info
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = teacher
        fields = ['name']
