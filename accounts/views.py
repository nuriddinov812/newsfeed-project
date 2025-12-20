from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import LoginForm,UserRegistrationForm,ProfileEditForm,UserProfileEditForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.views import View
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             print(cd)
#             user = authenticate(username=cd['username'],password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request,user)
#                     return HttpResponse('Authenticated successfully')
#                 else:
#                     return HttpResponse('Disabled account')
#             else:
#                 return HttpResponse('Invalid login')
#     else:
#         form = LoginForm()

#     return render(request,'accounts/login.html',{'form':form})

def dashboard(request):
    # Show the profile for the currently logged-in user
    user = request.user
    profile = None
    if request.user.is_authenticated:
        profile = getattr(request.user, 'profile', None)

    context = {
        'user': user,
        'profile': profile,
    }

    return render(request, 'pages/user_profile.html', context)



def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_user = User.objects.create_user(username=cd['username'],
                                                email=cd['email'],
                                                password=cd['password'],
                                                first_name=cd['first_name'],
                                                last_name=cd['last_name'])
            
            Profile.objects.create(user=new_user)
            
            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})
    
    
    
    
# class UserRegisterView(CreateView):
#     form_class = UserCreationForm
#     syccess_url = 'login/'
#     template_name = 'registration/register.html'



@login_required
def edit_user(request):

    profile = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = ProfileEditForm(instance=request.user, data=request.POST)
        profile_form = UserProfileEditForm(instance=profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('user_profile')
    else:
        user_form = ProfileEditForm(instance=request.user)
        profile_form = UserProfileEditForm(instance=profile)

    return render(request, 'account/profile_edit.html', {'user_form': user_form, 'profile_form': profile_form, 'profile': profile}) 



class EditUserView(View):
    
    def get(self, request):
        user_form = ProfileEditForm(instance=request.user)
        profile_form = UserProfileEditForm(instance=request.user.profile)
        return render(request, 'account/profile_edit.html', {'user_form': user_form, 'profile_form': profile_form})