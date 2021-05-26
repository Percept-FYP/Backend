from django.urls import path
from . import views


urlpatterns = [
    # path('test/<str:pk>/', views.test, name="test"),
    path('post', views.post, name="post"),


]
