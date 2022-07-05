from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from blogapp.forms import UserRegistrationForm,LoginForm,UserProfileForm
from django.views.generic import View, CreateView, FormView, TemplateView
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.urls import reverse_lazy
from blogapp.models import UserProfile
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

class IndexView(TemplateView):
    template_name="home.html"

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




