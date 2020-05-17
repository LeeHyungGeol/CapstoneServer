from django.urls import path
from . import views

urlpatterns = [
    path('marker/', views.MarkerAPIView.as_view()),
    path('measure/', views.MeasureAPIView.as_view()),

]