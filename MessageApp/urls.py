from django.urls import path
from . import views

urlpatterns = [
    path('message/', views.AllMessageListAPIVIEW.as_view()),
    path('message/<str:user_id>/', views.MessageListAPIView.as_view()),
    path('message/detail/<int:message_idx>/', views.MessageDetailAPIView.as_view()),


]