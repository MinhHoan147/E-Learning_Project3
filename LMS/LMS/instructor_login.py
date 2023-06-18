import re
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from app.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate,login,logout
from django.utils.safestring import mark_safe

def REGISTER(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        cv  = request.POST.get('CV')

        # check email
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already exist!')
            return redirect('become_instructor')

        # check username
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already exist!')
            return redirect('become_instructor')
        
        #check password
        if password1 != password2:
            messages.error(request, 'Your password does not match')
            return redirect('become_instructor')
        else:
            if len(password1) < 10 or not re.findall('[A-Z]', password1) or not re.findall('[@#$%!^&*]', password1):
                messages.error(request, mark_safe('<b>Your password is invalid, it must satisfy the following factors:<b\>'))
                messages.warning(request, 
                               mark_safe('Containing at least 10 characters.<br/> Containing at least 1 uppercase letter.<br/> Containing at least 1 uppercase letter.<br/> Containing at least 1 special character'))
                return redirect('become_instructor')
        
        #check cv
        if cv == '':
            messages.error(request, 'Please upload your CV')
            return redirect('become_instructor')
        
        user = User(
            username=username,
            email=email,
        )
        user.set_password(password1)
        user.save()
        return redirect('login')

    return render(request,'registration/register.html')

def DO_LOGIN(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = EmailBackEnd.authenticate(request,
                                         username=email,
                                         password=password)
        print("------------------")
        print(email)
        print(password)
        print("======================")
        if user != None and email != "" and password != "":
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Email and Password Are Invalid !')
            return redirect('login')
        
# def DO_LOGIN_BLOG(request):
#     if request.method == "POST":
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         user = EmailBackEnd.authenticate(request,
#                                          username=email,
#                                          password=password)
#         if user != None:
#             login(request, user)
#             return redirect('home')
#         else:
#             messages.error(request, 'Email and Password Are Invalid !')
#             return redirect('loginBlog')

def PROFILE(request):
    return render(request,'registration/profile.html')

def PROFILE_UPDATE(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_id = request.user.id

        user = User.objects.get(id=user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email

        if password != None and password != "":
            user.set_password(password)
        user.save()
        messages.success(request, 'Profile Are Successfully Updated. ')
        return redirect('profile')