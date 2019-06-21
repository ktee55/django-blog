from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
# from django.contrib.auth.forms import UserCreationForm


def register(request):
  if request.method == 'POST':
    form = UserRegisterForm(request.POST)
    if form.is_valid():
      # form.save()
      # username = form.cleaned_data.get('username')
      # messages.success(request, f'Account created for {username}! You are now able to log in')
      # return redirect('login')
      ## To login automatically after registration
      new_user = form.save()
      messages.info(request, "Thanks for registering. You are now logged in.")
      new_user = authenticate(username=form.cleaned_data['username'],
                              password=form.cleaned_data['password1'],
                              )
      login(request, new_user)
      return redirect('profile') #or blog-home, etc..
  else:
    form = UserRegisterForm()
  return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
  if request.method == 'POST':
    u_form = UserUpdateForm(request.POST, instance=request.user)
    p_form = ProfileUpdateForm(request.POST, 
                               request.FILES, 
                               instance=request.user.profile)
    if u_form.is_valid() and p_form.is_valid():
      u_form.save()
      p_form.save()
      messages.success(request, 'Your account has been updated!')
      return redirect('profile') #to avoid re-post request to the page( if reached to reander it will re-post)
  else:
    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)

  context = {
    'u_form': u_form,
    'p_form': p_form
  }

  return render(request, 'users/profile.html', context)

# def profiles(request, user_id):
#   try:
#     user = User.objects.get(pk=user_id)
#   except User.DoesNotExist:
#     raise Http404("User does not exist")
#   context = {
#     "user": user
#   }
#   return render(request, 'users/profiles.html', context)