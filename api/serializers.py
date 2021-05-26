from rest_framework import serializers
from .models import attendance,info


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = attendance
        fields = '__all__'

class infoSerializer(serializers.ModelSerializer):
    class Meta:
        model = info
        fields = '__all__'