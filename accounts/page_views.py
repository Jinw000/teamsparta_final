from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import TemplateView
from .models import User

# url 리다이렉트
def home(request):
    return render(request, 'home.html')

class SignupPageView(TemplateView):
    template_name = 'accounts/signup.html'

class LoginPageView(TemplateView):
    template_name = 'accounts/login.html'

class MainPageView(TemplateView):
    template_name = 'accounts/main.html'

class ProfilePageView(TemplateView):
    template_name = 'accounts/profile.html'