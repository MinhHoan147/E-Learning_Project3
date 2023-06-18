from django import forms
from django.contrib.auth.models import User
from app.models import *


class LearnerUserInfo(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput()) #hash out the password
    
    class Meta():
        model = User
        fields = ('username', 'email', 'password')

class LearnerSignUpForm(forms.ModelForm):
    class Meta():
        model = Learner
        fields = ('First_Name', 'Last_Name', 'gender')        
#_____________________________________________________________________________________________________________________

class InstructorUserInfo(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput()) #hash out the password
    
    class Meta():
        model = User
        fields = ('email', 'password')

class InstructorSignUpForm(forms.ModelForm):
    class Meta():
        model = Instructor
        fields = ('First_Name', 'Last_Name', 'gender', 'level', 'cv')
#_____________________________________________________________________________________________________________________

class InstructorCreateCourseForm(forms.ModelForm):
    # user = forms.ModelChoiceField(queryset=User.objects.all(), empty_label="Author", to_field_name="id")
    category = forms.ModelChoiceField(queryset=Categories.objects.all(), empty_label="Category", to_field_name="name")
    level = forms.ModelChoiceField(queryset=Level.objects.all(), empty_label="Level", to_field_name="name")
    language = forms.ModelChoiceField(queryset=Language.objects.all(), empty_label="Language", to_field_name="id")

    class Meta:
        model = Course
        fields =['featured_video', 'title', 'description', 'price', 'discount', 'deadline', 'slug']

class InstructorCreateLessonForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), empty_label="Course", to_field_name="id")
    
    class Meta:
        model = Lesson
        fields =['name']
        
class InstructorCreateQuizzForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), empty_label="Course", to_field_name="id")
    lesson = forms.ModelChoiceField(queryset=Lesson.objects.all(), empty_label="Lesson", to_field_name="id")
    
    class Meta:
        model = Quizzes
        fields =['slug', 'topic', 'number_of_questions', 'time_duration', 'require_passing_score', 'total_attempts', 'difficulty_level']       

class InstructorCreateVideoForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), empty_label="Course", to_field_name="id")
    lesson = forms.ModelChoiceField(queryset=Lesson.objects.all(), empty_label="Lesson", to_field_name="name")
    
    class Meta:
        model = Video
        fields =['serial_number', 'title', 'description', 'youtube_id', 'time_duration', 'preview']   

# GENDER =(
#     ("Male", "Male"),
#     ("Female", "Female"),
#     ("Other", "Other"),
# )
# Time = [
#     ("10:00 A.M","10:00 A.M")
#     # ("10:30 A.M","10:30 A.M"),
#     ("11:00 A.M","11:00 A.M"),
#     # ("11:30 A.M","11:30 A.M"),
#     ("12:00 P.M","12:00 P.M"),
#     # ("12:30 P.M","12:30 P.M"),
#     ("01:00 P.M","01:00 P.M"),
#     # ("01:30 P.M","01:30 P.M"),
#     # ("05:00 P.M","05:00 P.M"),
#     ("05:30 P.M","05:30 P.M"),
#     # ("06:00 P.M","06:00 P.M"),
#     ("06:30 P.M","06:30 P.M"),
#     # ("07:00 P.M","07:00 P.M"),
#     ("07:30 P.M","07:30 P.M"),
#     # ("08:00 P.M","08:00 P.M"),
#     ("08:30 P.M","08:30 P.M"),
# ]

# class NormalUserInfo(forms.ModelForm):
#     password = forms.CharField(widget = forms.PasswordInput()) #hash out the password
    
#     class Meta():
#         model = User
#         fields = ('username','email','password')

# class NormalUserSignUpForm(forms.ModelForm):
#     class Meta():
#         model = NormalUser
#         fields = ('username','email', 'gender', 'contact', 'address')        
# #_____________________________________________________________________________________________________________________

# class InstructorInfo(forms.ModelForm):
#     password = forms.CharField(widget = forms.PasswordInput()) #hash out the password
    
#     class Meta():
#         model = User
#         fields = ('username','email','password')

# class InstructorInfoSignUpForm(forms.ModelForm):
#     class Meta():
#         model = Instructor
#         fields = ('username','email','gender', 'contact', 'address', 'CV')     
        
# #_____________________________________________________________________________________________________________________
# class AdminUserInfo(forms.ModelForm):
#     password = forms.CharField(widget = forms.PasswordInput()) #hash out the password
    
#     class Meta():
#         model = User
#         fields = ('username','password')

# class AdminSignUpForm(forms.ModelForm):
#     class Meta():
#         model = User
#         fields = ('first_name','last_name','username','password')
# #_____________________________________________________________________________________________________________________

# class AppointmentForm(forms.ModelForm):
#     doctorId=forms.ModelChoiceField(queryset=Doctor.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
#     patientId=forms.ModelChoiceField(queryset=Patient.objects.all().filter(status=True),empty_label="Patient Name", to_field_name="user_id")
#     appointmentDate = forms.DateField(widget = forms.SelectDateWidget())
#     class Meta:
#         model=Appointment
#         fields=['appointmentDate','time','description']

# class PatientAppointmentForm(forms.ModelForm):
#     doctorId=forms.ModelChoiceField(queryset=Doctor.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
    
#     appointmentDate = forms.DateField(widget = forms.SelectDateWidget())
#     class Meta:
#         model=Appointment
#         fields=['appointmentDate','time','description']

#_____________________________________________________________________________________________________________________
