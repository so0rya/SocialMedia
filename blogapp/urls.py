from django.urls import path
from blogapp import views
urlpatterns=[
    path("accounts/signup", views.SignUpView.as_view(), name="sign-up"),
    path("accounts/signin", views.SignInView.as_view(), name="sign-in"),
    path("home", views.IndexView.as_view(), name="home"),
    path("users/profile/add",views.CreateUserProfileView.as_view(),name="add-profile"),
    path("users/profiles",views.ViewMyProfile.as_view(),name="view-my-profile"),
    path("users/profiles/pssword-reset",views.ChangePasswordView.as_view(),name="password-change"),
    path("users/profile/update<int:user_id>",views.ProfileUpdateView.as_view(),name="profile-update"),
    path("post/comment/<int:post_id>",views.add_comment,name="add-comment"),
    path("post/like/<int:post_id>", views.add_like,name="add-like")

]