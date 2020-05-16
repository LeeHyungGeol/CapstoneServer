from . import views
from django.urls import path

urlpatterns = [
    path('textVoiceDischargeTips/', views.TextVoiceDischargeTipsView.as_view()),
    path('imageDischargeTips/', views.ImageDischargeTipsView.as_view()),
]