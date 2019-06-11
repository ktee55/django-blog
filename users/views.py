from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .forms import UserRegisterForm
# from django.contrib.auth.forms import UserCreationForm


def register(request):
  if request.method == 'POST':
    form = UserRegisterForm(request.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data.get('username')
      messages.success(request, 'Your account has been created! You are now able to log in')
      return redirect('login')
      # # To login automatically after registration
      # new_user = form.save()
      # messages.info(request, "Thanks for registering. You are now logged in.")
      # new_user = authenticate(username=form.cleaned_data['username'],
      #                         password=form.cleaned_data['password1'],
      #                         )
      # login(request, new_user)
      # return redirect('profile')
  else:
    form = UserRegisterForm()
  return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
  return render(request, 'users/profile.html')
