from django.urls import path
from .views import HelloAPI, RegistrationAPI, LoginAPI, UserAPI, UserProfileView, UserShareCompleteCheckView, UserShareListView
from knox import views as knox_views

urlpatterns = [
    path("hello/", HelloAPI),
    path("auth/register/", RegistrationAPI.as_view()),
    path("auth/user/", UserAPI.as_view()),
    path("auth/login/", LoginAPI.as_view(), name='knox_login'),
    path("auth/logout/", knox_views.LogoutView.as_view(), name='knox_logout'),
    path("auth/logoutAll/", knox_views.LogoutAllView.as_view(), name='knox_logoutAll'),
    path('userprofile/', UserProfileView.as_view()),
    path('usersharelist/', UserShareListView.as_view()),
    path('usersharecheck/<int:idx>/', UserShareCompleteCheckView.as_view()),

]