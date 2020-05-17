from django.urls import path
from . import views

urlpatterns = [
    path('community/', views.CommunityListAPIView.as_view()),
    path('community/detail/<int:idx>/', views.CommunityDetailAPIView.as_view()),
    path('community/<str:user_id>/', views.CommunityUserListAPIView.as_view()),

]