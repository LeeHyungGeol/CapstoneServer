from . import views
from django.urls import path

urlpatterns = [
    path('location_waste_information/', views.LocationWasteInformationView.as_view()),

]