from django.shortcuts import render
from django.views import View

# url 리다이렉트
def home(request):
    return render(request, 'home.html')

class SignupPageView(View):
    def get(self, request):
        return render(request, 'accounts/signup.html')

class LoginPageView(View):
    def get(self, request):
        return render(request, 'accounts/login.html')

class MainPageView(View):
    def get(self, request):
        return render(request, 'accounts/main.html')