from rest_framework import serializers
from .models import attendance, info, teacher, Class, attendance, Student, Subject, User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


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
        print("thi s", attendances_data)
        ClASS = Class.objects.create(**validated_data)
        for attendance_data in attendances_data:
            print("thi s", attendance_data)
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

####################


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)
        data.update({'user': self.user.username})
        data.update({'id': self.user.id})
        data.update({'role': self.user.role})

        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['role'] = user.role
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    token_obtain_pair = TokenObtainPairView.as_view()

#####registr#####


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'password2',
                  'email', 'first_name', 'last_name', 'role')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            # first_name=validated_data['first_name'],
            # last_name=validated_data['last_name'],
            # role=validated_data['role']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

# {
# "username":"xai",
# "password":"1234",
# "password2":"1234",
# "email":"xaib@gmail.com",
# "first_name":"syed",
# "last_name":"zaiban",
# "role":"student",
# }
