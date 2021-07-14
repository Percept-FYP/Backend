
from django.shortcuts import render
from api.recognize_faces_image import func
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, DjangoMultiPartParser
from rest_framework.decorators import api_view
from api.serializers import AttendanceSerializer, ClassSerializer, RegisterSerializer, SubjectsSerializer, Time_tableSerializer
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from api.models import *
import PIL.Image
import openpyxl
import datetime
from django.core.files.base import File
import os
from pathlib import Path
from rest_framework import status
BASE_DIR = Path(__file__).resolve().parent.parent


@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    print(serializer)
    if serializer.is_valid(raise_exception=True):
        print("were hered")

        serializer.save()
        print(serializer.data)
        return Response(serializer.data)
    else:
        return Response("not created")


@api_view(['POST'])
def user_details(request):
    id = request.data['user_id']
    first_name = request.data['first_name']
    last_name = request.data['last_name']
    role = request.data['role']
    phone = request.data['phone']
    try:
        designation = request.data["designation"]
    except:
        designation = "null"
    try:
        usn = request.data['usn']
        sem = request.data['sem']
        branch = request.data['branch']
    except:
        usn = "null"
    user = User.objects.get(id=id)
    user.first_name = first_name
    user.last_name = last_name
    user.role = role
    user.phone = phone
    user.save()
    if user.role == "teacher":
        Teacher = teacher.objects.create(user=user, designation=designation)
        return Response("you are a teacher now")
    elif user.role == "student" and usn != "null":

        student = Student.objects.create(
            user=user, usn=usn, name=first_name, academic_info=Academic_info.objects.get(branch=branch))
        student.academic_info.semester = sem

        student.save()
        return Response("you are a student")
    else:
        return Response("no role created")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post(request):
    data = request.data
    CLASS = Class.objects.create(subject=Subject.objects.get(
        subject_code=data["class_name"]), image=data["image"], image1=data["image1"], image2=data["image2"])
    id = CLASS.id
    serializer = ClassSerializer(CLASS)
    if serializer:
        print("valid")
        list_all = []
        for e in Student.objects.all().order_by("id"):
            list_all.append(e.usn)
        images = []
        images.append(CLASS.image)
        images.append(CLASS.image1)
        images.append(CLASS.image2)

        file = CLASS.subject.attendance_file
        print(file)
        present_list = []
        for img in images:
            present_list = present_list + func(img)
        print("present_list", present_list)
        abs_list = list(set(list_all) - set(present_list)) + \
            list(set(present_list) - set(list_all))
        class_na = data["class_name"]

        present_list = list(set(present_list))
        try:
            present_list.remove('Unknown')
        except:
            pass
        try:
            abs_list.remove('Unknown')
        except:
            pass
        for usn in present_list:
            print(usn)
            attend = attendance.objects.create(
                student=Student.objects.get(usn=usn), attend="present", Class=Class.objects.get(id=id))
        for usn in abs_list:
            print(usn)
            attend = attendance.objects.create(
                student=Student.objects.get(usn=usn), attend="absent", Class=Class.objects.get(id=id))
        attendances = attendance.objects.filter(
            Class=id).order_by("student")
        pth = os.path.join(BASE_DIR, "static\\media\\")+str(file)
        p = pth.replace("/", "\\")

        filename = str(CLASS.subject)

        exl = p.replace("somefile1", filename)
        print(exl)

        workbook1 = openpyxl.load_workbook(exl)
        worksheet1 = workbook1['Sheet1']
        # get the number of columns filled
        ncol = worksheet1.max_column

        row = 0
        column = 0

        # Get the currennt date
        today = datetime.date.today().strftime("%d-%m-%Y")
        wbkName = exl
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
    CS = ClassSerializer(instance=CLASS)
    print(CS.data)
    serializer = AttendanceSerializer(attendances, many=True)
    print(serializer.data)
    return Response(CS.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update(request, cl):
    # attendances = attendance.objects.filter(Class=cl).delete()
    attendancse = request.data['attendance_set']
    clas = Class.objects.get(id=cl)
    file = clas.subject.attendance_file
    # serializer = ClassSerializer(instance=clas, data=request.data)
    for atd in attendancse:
        id = atd['id']
        isinst = attendance.objects.get(id=id)
        serializer2 = AttendanceSerializer(instance=isinst, data=atd)
        if serializer2.is_valid():
            serializer2.save()
    if serializer2.is_valid():
        serializer2.save()
        present_list = []
        list_all = []
        attends = attendance.objects.filter(Class_id=cl, attend="present")
        for i in attends:
            present_list.append(i.student.usn)
        for e in Student.objects.all():
            list_all.append(e.usn)
        print(list_all)
        pth = os.path.join(BASE_DIR, "static\\media\\")+str(file)
        p = pth.replace("/", "\\")

        filename = str(clas.subject)

        exl = p.replace("somefile1", filename)
        print(exl)

        workbook1 = openpyxl.load_workbook(exl)
        worksheet1 = workbook1['Sheet1']
        # get the number of columns filled
        ncol = worksheet1.max_column

        row = 0
        column = 0

        # Get the currennt date
        today = datetime.date.today().strftime("%d-%m-%Y")
        wbkName = exl
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

    return Response("Sucessgully Updated", status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def subject_create(request):
    Teacher = teacher.objects.get(user=request.user)
    subject_name = request.data['subject_name']
    subject_code = request.data['subject_code']
    sem = request.data['sem']
    branch = request.data['branch']
    subject = Subject.objects.create(teacher=Teacher,
                                     subject_name=subject_name, subject_code=subject_code, academic_info=Academic_info.objects.get(branch=branch))
    subject.academic_info.semester = sem

    subject.save()
    return Response("subject added")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def subjects(request):
    if request.user.role == "teacher":
        print('teacher')
        subjects = Subject.objects.filter(
            teacher=teacher.objects.get(user=request.user))
        print(subjects)
        serializer = SubjectsSerializer(subjects, many=True)
        return Response(serializer.data)
    elif request.user.role == "student":
        print('students')
        student = Student.objects.get(user=request.user)
        academic_info = student.academic_info
        subjects = Subject.objects.filter(
            academic_info=academic_info)
        print(subjects)
        serializer = SubjectsSerializer(subjects, many=True)
        return Response(serializer.data)
    else:
        print('no role')
        return Response("no role set")


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def attendance_details(request, cl):

    if request.method == 'GET':
        user = request.user
        student = Student.objects.get(user=user)
        Clasess = Class.objects.filter(
            subject=Subject.objects.get(subject_code=cl))
        attendances = []
        for CLASS in Clasess:
            Attendance = attendance.objects.filter(
                student=student, Class=CLASS)
            serializer = AttendanceSerializer(Attendance, many=True)
            attendances = attendances + serializer.data
        print(attendances)
        return Response(attendances)

    elif request.method == 'POST':
        usn = request.data['usn']
        student = Student.objects.get(usn=usn)
        Clasess = Class.objects.filter(
            subject=Subject.objects.get(subject_code=cl))
        attendances = []
        for CLASS in Clasess:
            Attendance = attendance.objects.filter(
                student=student, Class=CLASS)
            serializer = AttendanceSerializer(Attendance, many=True)
            attendances = attendances + serializer.data
        print(attendances)
        return Response(attendances, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def attendance_overview(request):
    user = request.user
    student = Student.objects.get(user=user)
    Academic_info = student.academic_info
    subjects = Subject.objects.filter(academic_info=Academic_info)
    result_set = []
    for subject in subjects:
        present_count = 0
        absent_count = 0
        all = 0
        Clasess = Class.objects.filter(
            subject=subject)
        for CLASS in Clasess:
            print(CLASS)
            all = all + 1

            present_count = present_count + attendance.objects.filter(
                student=student, Class=CLASS, attend="present").count()
            print(present_count)
            absent_count = absent_count + attendance.objects.filter(
                student=student, Class=CLASS, attend="absent").count()
            print(absent_count)

        print("subject:", str(subject), "present:", present_count,
              "absent:", absent_count)
        print("total", present_count+absent_count)
        if present_count > 0:
            # have to change!
            percentage = (present_count/(present_count+absent_count))*100
        else:
            percentage = 0
        result = {
            "subject": str(subject),
            "classes attended":  present_count,
            "classes taken": all,
            "%": round(percentage, 2)
        }
        result_set.append(result)
    attendances_overview = []

    return Response(result_set)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def attendance_filter(request):
    date = request.data['date']
    Sub = request.data['subject']
    user = request.user
    student = Student.objects.get(user=user)
    Clasess = Class.objects.filter(
        subject=Subject.objects.get(subject_code=Sub), time__date=date)
    attendances = []
    for CLASS in Clasess:
        Attendance = attendance.objects.filter(
            student=student, Class=CLASS)
        serializer = AttendanceSerializer(Attendance, many=True)
        attendances = attendances + serializer.data
    print(attendances)
    return Response(attendances)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def attendance_filter(request):
    user = request.user
    student = Student.objects.get(user=user)
    Academic_info = student.Academic
    Clasess = Class.objects.filter(
        subject=Subject.objects.get(subject_code=Sub), time__date=date)
    attendances = []
    for CLASS in Clasess:
        Attendance = attendance.objects.filter(
            student=student, Class=CLASS)
        serializer = AttendanceSerializer(Attendance, many=True)
        attendances = attendances + serializer.data
    print(attendances)
    return Response(attendances)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def time_table(request):
    user = request.user
    if user.role == "student":
        student = Student.objects.get(user=user)
        academic_info = student.academic_info.id
        print("academic", academic_info)
        subjects = Subject.objects.filter(academic_info=academic_info)
        time_table = []
        for subject in subjects:
            print(subject)
            time_tables = Time_table.objects.filter(subject=subject)
            serializer = Time_tableSerializer(time_tables, many=True)
            print(serializer.data)
            time_table = time_table + serializer.data
        print(time_table)
        return Response(time_table)

    else:
        id = user.id
        Teacher = teacher.objects.get(user=id)
        subjects = Subject.objects.filter(teacher=Teacher)
        time_table = []
        for subject in subjects:
            print(subject)
            time_tables = Time_table.objects.filter(subject=subject)
            serializer = Time_tableSerializer(time_tables, many=True)
            print(serializer.data)
            time_table = time_table + serializer.data
        print(time_table)
        return Response(time_table)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recent_class(request):
    id = request.user.id
    Teacher = teacher.objects.get(user=id)
    print("teacher", Teacher)
    recent_class = Class.objects.filter(subject__teacher__user=id).last()
    print("recent_Class", recent_class)
    present_count = attendance.objects.filter(
        Class=recent_class, attend="present").count()
    print("p", present_count)

    absent_count = attendance.objects.filter(
        Class=recent_class, attend="absent").count()
    print("a", absent_count)
    percentage = (present_count/(present_count+absent_count))*100
    print("percentage", percentage)
    return Response(percentage)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def teacher_schedule(request):
    day = request.data['day']
    id = request.user.id
    schedule = Time_table.objects.filter(day=day, subject__teacher__user=id)
    serializer = Time_tableSerializer(schedule, many=True)
    return Response(serializer.data)
