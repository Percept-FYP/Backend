from django.shortcuts import render
from api.recognize_faces_image import func
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.serializers import AttendanceSerializer,infoSerializer
from api.models import *
from PIL import Image
import cv2

# Create your views here.


# @api_view(['GET'])
# def test(request, pk="A2"):
#     list = func()
#     print(list)
#     print(len(list))
#     list_all = []

#     for e in Student.objects.all():
#         list_all.append(e.usn)
#     print(list_all)
#     abs_list = set(list) ^ set(list_all)
#     print(abs_list)
#     for usn in list:
#         attend = attendance.objects.create(
#             usn=usn, attend="present", class_id=pk)
#     for usn in abs_list:
#         attend = attendance.objects.create(usn=usn, attend="absent", class_id=pk)
#     attendances = attendance.objects.filter(class_id=pk)

#     serializer = AttendanceSerializer(attendances, many=True)
#     return Response(serializer.data)

@api_view(['POST'])
def post(request):
    print("was here")
    serializer = infoSerializer(data=request.data)
    if serializer.is_valid():
        print("valid")
        serializer.save()
        infos = info.objects.last() 
        img = infos.image
        print(img)
        list = func(img)
        print(list)

    return Response(request.data)
