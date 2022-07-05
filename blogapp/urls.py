from django.urls import path
from blogapp import views
urlpatterns=[
    path("accounts/signup", views.SignUpView.as_view(), name="sign-up"),
    path("accounts/signin", views.SignInView.as_view(), name="sign-in"),
    path("home", views.IndexView.as_view(), name="home"),
    path("users/profile/add",views.CreateUserProfileView.as_view(),name="add-profile"),


]