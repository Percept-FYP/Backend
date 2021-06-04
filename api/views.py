from django.shortcuts import render
from api.recognize_faces_image import func
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.serializers import AttendanceSerializer, infoSerializer, ClassSerializer
from api.models import *
import PIL.Image
import cv2
import openpyxl
import datetime


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
    data = request.data

    # {"teacher":"teacher_name",   
    # "subject_code":"17cs05"
    # "image":""}
    print(data)
    
    CLASS = Class.objects.create(subject=Subject.objects.get(subject_code=data["class_name"]),image=data["image"])
    imagee = request.data["image"]
    # print(imagee)
    # cv2.imshow("Image", imagee)
    serializer = ClassSerializer(CLASS)
    if serializer:
        print("valid")
        list_all = []
        for e in Student.objects.all().order_by("id"):
            list_all.append(e.usn)
        # print(list_all)
        infos = info.objects.last()
        img = infos.image
        print(img)
        # im=PIL.Image.open(imagee)
        # im.show()
        present_list = func(img)
        abs_list = list(set(list_all) - set(present_list)) + \
            list(set(present_list) - set(list_all))
        class_na = infos.class_name
        print(type(present_list))
        present_list = list(set(present_list))
        present_list.remove('Unknown')
        abs_list.remove('Unknown')
        for usn in present_list:
            attend = attendance.objects.create(
                usn=usn, attend="present", class_id=class_na)
        for usn in abs_list:
            attend = attendance.objects.create(
                usn=usn, attend="absent", class_id=class_na)
        attendances = attendance.objects.filter(
            class_id=class_na).order_by("usn")
        workbook1 = openpyxl.load_workbook(
            'D:/FYP/main/backend/_backend/DB.xlsx')
        worksheet1 = workbook1['Sheet1']
        # get the number of columns filled
        ncol = worksheet1.max_column

        row = 0
        column = 0

        # Get the currennt date
        today = datetime.date.today().strftime("%d-%m-%Y")
        wbkName = 'DB.xlsx'
        wbk = openpyxl.load_workbook(wbkName)

        # Loop through the usn and write to the column 1
        for wks in wbk.worksheets:
            i = 0
            wks.cell(row=i+1, column=1).value = "USN"
            while i < len(list_all):
                wks.cell(row=i+2, column=1).value = list_all[i]
                i += 1

        # Check the result names and assign the attendance in the excel sheet
        for wks in wbk.worksheets:
            i = 0
            wks.cell(row=i+1, column=ncol+1).value = today
            while i < len(list_all):
                if list_all[i] in present_list:
                    wks.cell(row=i+2, column=ncol+1).value = "Present"
                else:
                    wks.cell(row=i+2, column=ncol+1).value = "Absent"
                i += 1

        # Save the workbook
        wbk.save(wbkName)
        wbk.close
    print(abs_list)
    print(present_list)
    serializer = AttendanceSerializer(attendances, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def update(request, cl):
    print(request.data)
    attendances = attendance.objects.filter(class_id=cl).delete()
    serializer = AttendanceSerializer(data=request.data, many=True)
    print(repr(serializer))
    if serializer.is_valid():
        print("in serial")
        serializer.save()
        present_list = []
        list_all = []
        attends = attendance.objects.filter(class_id=cl, attend="present")
        for i in attends:
            present_list.append(i.usn)
        print(present_list)
        for e in Student.objects.all():
            list_all.append(e.usn)
        workbook1 = openpyxl.load_workbook(
            'D:/FYP/main/backend/_backend/DB.xlsx')
        worksheet1 = workbook1['Sheet1']
        # get the number of columns filled
        ncol = worksheet1.max_column

        row = 0
        column = 0

        # Get the currennt date
        today = datetime.date.today().strftime("%d-%m-%Y")
        wbkName = 'DB.xlsx'
        wbk = openpyxl.load_workbook(wbkName)

        # Loop through the usn and write to the column 1
        for wks in wbk.worksheets:
            i = 0
            wks.cell(row=i+1, column=1).value = "USN"
            while i < len(list_all):
                wks.cell(row=i+2, column=1).value = list_all[i]
                i += 1

        # Check the result names and assign the attendance in the excel sheet
        for wks in wbk.worksheets:
            i = 0
            wks.cell(row=i+1, column=ncol).value = today
            while i < len(list_all):
                if list_all[i] in present_list:
                    wks.cell(row=i+2, column=ncol).value = "Present"
                else:
                    wks.cell(row=i+2, column=ncol).value = "Absent"
                i += 1

        # Save the workbook
        wbk.save(wbkName)
        wbk.close

    return JsonResponse("updated successfully!", safe=False)
