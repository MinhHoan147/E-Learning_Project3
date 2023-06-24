import re
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from LMS.forms import InstructorSignUpForm, InstructorUserInfo, LearnerSignUpForm, LearnerUserInfo
from app.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate,login,logout
from django.utils.safestring import mark_safe
from . import candy
from app.models import *

def REGISTER(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
      
        # check email
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already exist!')
            return redirect('register')

        # check username
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already exist!')
            return redirect('register')
        
        #check password
        if password1 != password2:
            messages.error(request, 'Your password does not match')
            return redirect('register')
        
        else:
            if len(password1) < 10 or not re.findall('[A-Z]', password1) or not re.findall('[@#$%!^&*]', password1):
                messages.error(request, mark_safe('<b>Your password is invalid, it must satisfy the following factors:<b\>'))
                messages.warning(request, 
                               mark_safe('Containing at least 10 characters.<br/> Containing at least 1 uppercase letter.<br/> Containing at least 1 uppercase letter.<br/> Containing at least 1 special character'))
                return redirect('register')

        user = User(
            username=username,
            email=email,
        )
        user.set_password(password1)
        user.save()
        return redirect('login')

    return candy.render(request,'registration/register.html')

def DO_LOGIN(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password') 
        role = request.POST.get('role')
        myUser = EmailBackEnd.authenticate(request,
                                         email=email,
                                         password=password)
        
        myRole = UserRole.objects.filter(user = myUser)
        if myUser != None and email != "" and password != "" and role != "":
                if myUser.is_active:
                    if str(myRole[0].role) == role:
                        if role == 'Learner':      
                            login(request, myUser)  
                            return redirect('home') 
                        if role == 'Instructor':
                            login(request, myUser) 
                            return redirect('instructor-dashboard')
                        else:
                            messages.error(request, 'You tried to log in with the wrong permissions !')
                            return candy.render(request,'registration/login.html')    
                    else:
                        messages.error(request, 'You tried to log in with the wrong permissions !')
                        return candy.render(request,'registration/login.html')     
                else:
                    messages.error(request, 'Your account has not been activated !')
                    return candy.render(request,'registration/login.html')     
        else:
            messages.error(request, 'Email/Password Is Invalid !')
            return candy.render(request,'registration/login.html')
    else:
        return candy.render(request,'registration/login.html')
        
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
    return candy.render(request,'registration/profile.html')

def PROFILE_UPDATE(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_id = request.user.id

        user = User.objects.get(id = user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email

        if password != None and password != "":
            user.set_password(password)
        user.save()
        messages.success(request, 'Profile Are Successfully Updated.')
        return redirect('profile')

def LEARNER_SIGNUP(request):

    if request.method == "POST":
 
        #Validate input
        username = request.POST.get('username')
        email = request.POST.get('email')
        firstName = request.POST.get('First_Name')
        lastName = request.POST.get('Last_Name')
        password = request.POST.get('password1')
        re_password = request.POST.get('password2')
        gender = request.POST.get('gender')

        # check email
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already exist')
            return redirect('register')

        # check username
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already exist')
            return redirect('register')
        
        # check firstName and lastName
        if not firstName.isalpha() or not lastName.isalpha():
            messages.error(request, 'First and Last Name can only contain characters')
            return redirect('register')
    
        #check password
        if password != re_password:
            messages.error(request, 'Your password does not match')
            return redirect('register')
        
        else:
            if len(password) < 10 or not re.findall('[A-Z]', password) or not re.findall('[0-9]', password) or not re.findall('[@#$%!^&*]', password):
                messages.error(request, mark_safe('<b>Your password is invalid, it must satisfy the following factors:<b\>'))
                messages.warning(request, 
                               mark_safe('Containing at least 10 characters.<br/> Containing at least 1 uppercase letter.<br/> Containing both letters and numbers.<br/> Containing at least 1 special character'))
                return redirect('register')
            
        user = User(
            username=username,
            email=email,
            is_active=False
        )

        user.set_password(password)
        user.save()
      
        learner = Learner(
            user=user,
            First_Name= firstName,
            Last_Name = lastName,
            gender = gender,
            role = Role.objects.get(role = "Learner")
        )
        learner.save()
    
        userRole = UserRole(
            user=user,
            role=learner.role
        )
        userRole.save()
        
        return redirect('login')

    return candy.render(request,'registration/register.html')

# def LearnerLogin(request):
#     if request.method=="POST":
#         email = request.POST.get('email') 
#         password = request.POST.get('password')

#         user = authenticate(email = email, password=password)
        
#         if user:
#             if user.is_active:
#                 login(request, user) #login is the django's default function
                
#                 return HttpResponseRedirect(reverse('MyApp:afterlogin_view'))

#             else: 
#                 return HttpResponse("Account not Active")
        
#         else:
#             print("Someone tried to login and failed")
#             print("Username: {} and password {}".format(email,password))
#             return HttpResponse("Invalid Login details supplied!")
#     else:
#         return render('login')
    
def INSTRUCTOR_SIGNUP(request):
   if request.method == "POST":
        #Validate input
        username = request.POST.get('username')
        email = request.POST.get('email')
        firstName = request.POST.get('First_Name')
        lastName = request.POST.get('Last_Name')
        password = request.POST.get('password1')
        re_password = request.POST.get('password2')
        gender = request.POST.get('gender')
        cv = request.POST.get('cv')

        print(gender)
        print(cv)

        # check email
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already exist')
            return redirect('register')

        # check username
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already exist')
            return redirect('register')
        
        # check firstName and lastName
        if not firstName.isalpha() or not lastName.isalpha():
            messages.error(request, 'First and Last Name can only contain characters')
            return redirect('register')
    
        #check password
        if password != re_password:
            messages.error(request, 'Your password does not match')
            return redirect('register')
        
        else:
            if len(password) < 10 or not re.findall('[A-Z]', password) or not re.findall('[0-9]', password) or not re.findall('[@#$%!^&*]', password):
                messages.error(request, mark_safe('<b>Your password is invalid, it must satisfy the following factors:<b\>'))
                messages.warning(request, 
                               mark_safe('Containing at least 10 characters.<br/> Containing at least 1 uppercase letter.<br/> Containing both letters and numbers.<br/> Containing at least 1 special character'))
                return redirect('register')
            
        user = User(
            username=username,
            email=email,
            is_active=False
        )
        user.set_password(password)
        user.save()

        instructor = Instructor(
            user=user,
            First_Name= firstName,
            Last_Name = lastName,
            gender = gender,
            cv = "/Media/authorCV/" + cv,
            role = Role.objects.get(role = "Instructor")
        )
        instructor.save()

        userRole = UserRole(
            user=user,
            role=instructor.role
        )
        userRole.save()

        return redirect('login')
   
   return candy.render(request,'registration/register.html')

# def InstructorLogin(request):
#     if request.method=="POST":
#         email = request.POST.get('email') 
#         password = request.POST.get('password')

#         user = authenticate(email = email, password=password)
        
#         if user:
#             if user.is_active:
#                 login(request, user) #login is the django's default function
                
#                 return HttpResponseRedirect(reverse('MyApp:afterlogin_view'))

#             else: 
#                 return HttpResponse("Account not Active")
        
#         else:
#             print("Someone tried to login and failed")
#             print("Username: {} and password {}".format(email,password))
#             return HttpResponse("Invalid Login details supplied!")
#     else:
#         return render('login')
    