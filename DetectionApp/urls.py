from django.urls import path
from . import views

urlpatterns = [
    path('detection/', views.DetectionAPIView.as_view()),
    # path('detection2/', views.DetectionAPIView2.as_view()),
    path('clean/', views.CleanDetectionAPIView.as_view()),

]