from django.contrib.auth.forms import UserChangeForm
from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from .forms import SignupForm
from .models import User
from django.contrib import messages
# Create your views here.


User = get_user_model()

class SignupView(CreateView):
    model = User
    form_class = SignupForm
    template_name="accounts/signup.html"

    def form_valid(self, form):
        user = form.save()
        auth_login(self.request, user)
        return redirect('main:main')

signup = SignupView.as_view()

class LoginView(auth_views.LoginView):
    template_name="accounts/login.html"
    redirect_authenticated_user = True    

login = LoginView.as_view()
    
logout = auth_views.LogoutView.as_view()

def profile(request):
    success_url = '/'
    return render(request, 'main/main.html', )
