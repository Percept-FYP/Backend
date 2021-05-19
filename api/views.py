from django.shortcuts import render
from api.recognize_faces_image import func
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.serializers import AttendanceSerializer
from api.models import *

# Create your views here.


@api_view(['GET'])
def test(request, pk="A2"):
    list = func()
    print(list)
    print(len(list))
    list_all = []

    for e in Student.objects.all():
        list_all.append(e.usn)
    print(list_all)
    abs_list = set(list) ^ set(list_all)
    print(abs_list)
    for usn in list:
        attend = attendance.objects.create(
            usn=usn, attend="present", class_id=pk)
    for usn in abs_list:
        attend = attendance.objects.create(
            usn=usn, attend="absent", class_id=pk)
    attendances = attendance.objects.all()

    serializer = AttendanceSerializer(attendances, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def AttendaceList(request):
    blogs = attendance.objects.all()
    serializer = AttendanceSerializer(blogs, many=True)
    return Response(serializer.data)
