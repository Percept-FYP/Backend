from django.urls import path
from . import views
from api.serializers import MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    # path('test/<str:pk>/', views.test, name="test"),
    path('post', views.post, name="post"),
    path('subject_create/', views.subject_create, name="subject_create"),
    path('subjects/', views.subjects, name="subjects"),
    path('register/', views.register, name="register"),
    path('register/details', views.user_details, name="user_details"),
    path('update/<str:cl>', views.update, name="update"),
    path('attendance_details/<str:cl>',
         views.attendance_details, name="attendance_details"),
    path('attendance_overview',
         views.attendance_overview, name="attendance_overview"),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


]
