from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from blogapp.forms import UserRegistrationForm,LoginForm,UserProfileForm, ChangePasswordForm, BlogForm, CommentForm
from django.views.generic import View, CreateView, FormView, TemplateView, UpdateView
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.urls import reverse_lazy
from blogapp.models import UserProfile, Blogs, Comments
from django.utils.decorators import method_decorator

def signinrqd(fn):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return fn(request, *args, **kwargs)
        else:
            messages.error(request, "You must login")
            return redirect("signin")
    return wrapper


class SignUpView(CreateView):
    form_class=UserRegistrationForm
    template_name="registration.html"
    model=User
    success_url= reverse_lazy("sign-in")

class SignInView(FormView):
    form_class=LoginForm
    template_name="sign-in.html"


    # def get(self,request,*args,**kwargs):
    #     form=LoginForm
    #     return render(request,self.template_name,{"form":form})
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            user=authenticate(request,username=username,password=password)
            if user:
                print("success")
                login(request,user)
                return redirect("home")
            else:
                return render(request,self.template_name,{"form":form})

@signinrqd
def sign_out(request,*args,**kwargs):
    logout(request)
    return redirect("sign-in")

class IndexView(CreateView):
    model=Blogs
    form_class = BlogForm
    success_url = reverse_lazy("home")
    template_name="home.html"

    def form_valid(self, form):
        form.instance.author=self.request.user
        self.object= form.save()
        messages.success(self.request,"post is published")
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        blogs=Blogs.objects.all().order_by("posted_date")
        context["blogs"]=blogs
        comment_form=CommentForm()
        context["comment_form"]=comment_form
        return context

class CreateUserProfileView(CreateView):
    model=User
    template_name = "addprofile.html"
    form_class = UserProfileForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.user=self.request.user
        messages.success(self.request,"profile has been added")
        self.object= form.save()
        return super().form_valid(form)

class ViewMyProfile(TemplateView):
    template_name = "view-profile.html"

class ChangePasswordView(FormView):
    form_class = ChangePasswordForm
    template_name = "change-password.html"
    def post(self, request, *args, **kwargs):
        form=ChangePasswordForm(request.POST)
        if form.is_valid():
            oldpassword=form.cleaned_data.get("oldpassword")
            password1=form.cleaned_data.get("password1")
            password2 = form.cleaned_data.get("password2")
            user=authenticate(request,username=request.user,password=oldpassword)
            if user:
                user.set_password(password2)
                user.save()
                messages.success(request,"password reset successfully")
                return redirect("home")
            else:
                messages.error(request,"password reset unsuccessful")
                return render(request,"change-password.html",{"form":form})

class ProfileUpdateView(UpdateView):
    form_class = UserProfileForm
    model = UserProfile
    template_name = "profile-update.html"
    success_url = reverse_lazy("home")
    pk_url_kwarg = "user_id"

    def form_valid(self, form):
        messages.success(request,"Profile Updated")
        self.object = form.save()
        return super().form_valid(form)

def add_comment(request,*args,**kwargs):
    if request.method=='POST':
        blog_id=kwargs.get("post_id")
        blog=Blogs.objects.get(id=blog_id)
        user=request.user
        comment=request.POST.get('comment')
        Comments.objects.create(blog=blog,user=user,comment=comment)
        messages.success(request,"comment added")
        return redirect("home")

def add_like(request,*args,**kwargs):
    blog_id=kwargs.get("post_id")
    blog=Blogs.objects.get(id=blog_id)
    blog.liked_by.add(request.user)
    blog.save()
    messages.success(request,"like added")
    return redirect("home")

