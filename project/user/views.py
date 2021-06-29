from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.views.generic import View
# Create your views here.


class RegisterView(View):

    def post(self, request, *args, **kwargs):

        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            data = form.cleaned_data
            username = data.get('username')
            messages.success(
                request, f'Account created! You can now Log in your account')
            return redirect('login')
        return render(request, 'user/register.html', {'form': form})

    def get(self, request, *args, **kwargs):
        form = UserRegisterForm()
        return render(request, 'user/register.html', {'form': form})
