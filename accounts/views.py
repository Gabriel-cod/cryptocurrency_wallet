from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic import CreateView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = AuthenticationForm()
        context = {
            'form': form
        }
        return render(request, 'accounts/login.html', context=context)
    
    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request=request, username=username, password=password)
        print(username, password, user)
        if user:
            login(request=request, user=user)
            return redirect('home')
        context = {
            'form': form
        }
        return render(request, 'accounts/login.html', context=context)


class RegisterCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'accounts/register.html'
    success_url = '/login/'


def logout_view(request):
    logout(request)
    return redirect('login')