from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import LoginForm,UserRegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView

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
    user = request.user


    context = {
        'user': user,
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
            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})
    
    
    
    
# class UserRegisterView(CreateView):
#     form_class = UserCreationForm
#     syccess_url = 'login/'
#     template_name = 'registration/register.html'