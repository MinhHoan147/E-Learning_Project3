from audioop import reverse
import datetime
from time import time
import numpy as np
from django.shortcuts import redirect, render
from app.EmailBackEnd import EmailBackEnd
from django.contrib.auth.models import User, Group
from app.models import *
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum
from django.contrib import messages
from . import candy
from .settings import *
# import razorpay
from django.contrib.auth.decorators import login_required
from LMS.forms import InstructorCreateCourseForm, InstructorCreateLessonForm, InstructorCreateQuizzForm, InstructorCreateVideoForm,LearnerSignUpForm, LearnerUserInfo, InstructorSignUpForm, InstructorUserInfo
from .generate_certification import generate_certificates

# Create your views here.

# client = razorpay.Client(auth=(KEY_ID,KEY_SECRET))

def BASE(request):
    return candy.render(request, 'base.html')

def BLOG(request):
    return render(request, 'registration/blog.html')

def EVENT(request):
    return render(request, 'Main/event_single.html')

def HOME(request):
    category = Categories.objects.all().order_by('id')[0:6]
    course = Course.objects.filter(status='PUBLISH').order_by('-id')
    instructor = Instructor.objects.all()
    user = request.user
    if user.id != None:
        role = UserRole.objects.filter(user=request.user)
    else:
        role = None
    context = {
        'category': category,
        'course': course,
        'user': user,
        'instructor': instructor,
        'role': role
    }
    return candy.render(request, 'Main/home.html', context)


def SINGLE_COURSE(request):
    category = Categories.get_all_category(Categories)
    level = Level.objects.all()
    course = Course.objects.all()
    context = {
        'category': category,
        'level': level,
        'course': course,
    }
    return render(request, 'Main/single_course.html', context)


def CONTACT_US(request):
    category = Categories.objects.all().order_by('id')[0:5]
    course = Course.objects.filter(status='PUBLISH').order_by('-id')

    context = {
        'category': category,
        'course': course,
    }
    return candy.render(request, 'Main/contact_us.html', context)


def ABOUT_US(request):
    category = Categories.objects.all().order_by('id')[0:5]
    course = Course.objects.filter(status='PUBLISH').order_by('-id')

    context = {
        'category': category,
        'course': course,
    }
    return candy.render(request, 'Main/about_us.html', context)


def BECOME_AN_INSTRUCTOR(request):
    return candy.render(request, 'Main/become_instructor.html')


def COMING_SOON(request):
    return candy.render(request, 'Main/coming_soon.html')


def filter_data(request):
    categories = request.GET.getlist('category[]')
    level = request.GET.getlist('level[]')
    if categories:
        course = Course.objects.filter(
            category__id__in=categories).order_by('-id')
    elif level:
        course = Course.objects.filter(level__id__in=level).order_by('-id')
    else:
        course = Course.objects.all().order_by('-id')
    context = {
        'course': course
    }

    t = render_to_string('ajax/course.html', context)

    return JsonResponse({'data': t})


def SEARCH_COURSE(request):
    query = request.GET['query']
    category = Categories.get_all_category(Categories)
    course = Course.objects.filter(title__icontains=query)
    try:
        status = request.GET['status']
        level = request.GET['level']
        category = request.GET['category']
    except:
        return candy.render(request, 'search/search.html', context)

    print("STATUS: ", status)
    print("LEVEL: ", level)
    print("CATEGORY: ", category)
    context = {
        'course': course,
        'category': category,
    }
    return candy.render(request, 'search/search.html', context)

def INSTRUCTOR_SEARCH_COURSE(request):
    query = request.GET['query']
    # levels = Level.objects.all()
    status = ""
    # level = ""
    courses = Course.objects.filter(title__icontains=query)
    try:
        status = request.GET['status']
        if status == "Confirmed":
            status = "PUBLISH"
        if status == "Pending":
            status = "DRAFT"
        print("STATUS: ", status)
    except:
        pass
    
    # try:
    #     level = request.GET['level']
    #     print("LEVEL: ", level)
    #     print("LEVEL: ", levels["level"])
    # except:
    #     pass

    if status != "All":
        courses = Course.objects.filter(title__icontains=query, status=status)

    # if level == "All" and status != "All":
    #     courses = Course.objects.filter(title__icontains=query, status=status)
    # elif level != "All" and status == "All":
    #     courses = Course.objects.filter(title__icontains=query, level=level)
    # elif level != "All" and status != "All":
    #     if level == "Beginner":
    #         courses = Course.objects.filter(title__icontains=query, level=1, status=status)
    #     if level == "Beginner":
    #         courses = Course.objects.filter(title__icontains=query, level=2, status=status)
    #     if level == "Beginner":
    #         courses = Course.objects.filter(title__icontains=query, level=3, status=status)

    context = {
        'courses': courses,
        # 'levels' : levels
    }
    
    return candy.render(request, 'instructor/course_search.html', context)

def INSTRUCTOR_SEARCH_LESSON(request):
    query = request.GET['query']
    # category = Categories.get_all_category(Categories)
    courses = Course.objects.filter(user=request.user)
    lessons = []
    for course in courses:
        temps = Lesson.objects.filter(name__icontains=query, course = course)
        lessons.append(temps)
    context = {
        'lessons': lessons,
        # 'category': category,
    }

    return candy.render(request, 'instructor/lesson_search.html', context)

def INSTRUCTOR_SEARCH_QUIZZ(request):
    query = request.GET['query']
    # category = Categories.get_all_category(Categories)
    courses = Course.objects.filter(user=request.user)
    quizzes = []
    for course in courses:
        temps = Quizzes.objects.filter(topic__icontains=query, course = course)
        quizzes.append(temps)

    context = {
        'quizzes': quizzes,
        # 'category': category,
    }

    return candy.render(request, 'instructor/quizz_search.html', context)

def INSTRUCTOR_SEARCH_VIDEO_LECTURE(request):
    query = request.GET['query']
    # category = Categories.get_all_category(Categories)
    courses = Course.objects.filter(user=request.user)
    videos = []
    for course in courses:
        temps = Video.objects.filter(title__icontains=query, course = course)
        videos.append(temps)
    context = {
        'videos': videos,
        # 'category': category,
    }

    return candy.render(request, 'instructor/video_search.html', context)

def COURSE_DETAILS(request, slug):
    courses = Course.objects.all()
    category = Categories.get_all_category(Categories)
    time_duration = Video.objects.filter(course__slug=slug).aggregate(sum=Sum('time_duration'))
    course_id = Course.objects.get(slug=slug)
    comments = Comment.objects.all()
    quizzes = Quizzes.objects.filter(course=course_id, status=True)
    result = None
  
    try:
        result = Result.objects.filter(user=request.user)
    except:
        pass

    certificate = None
    user = request.user
    if user.id == None:
        check_enroll = None
    else:
        try:
            check_enroll = UserCourse.objects.get(
                user=request.user, course=course_id)
        except UserCourse.DoesNotExist:
            check_enroll = None

    course = Course.objects.filter(slug=slug)
    if course.exists():
        course = course.first()
    else:
        return redirect('404')
    action = request.GET.get('action')

    user = User.objects.get(id=request.user.id)

    try:
        result = Result.objects.filter(user=request.user, course=course_id, passed=True)
        certificate = Certificate.objects.get(userID=user, courseID=course_id)
    except:
        pass

    date_text = datetime.datetime.now().strftime("%Y-%m-%d")
    print("RESULT", result)
    print("RESULT COUNT", result.count())
    print("QUIZZES COUNT", quizzes.count())
    print("CERTIFICATE", certificate)
    if result is not None and result.count() == quizzes.count() and certificate is None and course_id.has_certificate:
        
        Certificate.objects.create(userID=user, courseID=course_id)
        certificate = Certificate.objects.get(userID=user, courseID=course_id)
        generate_certificates(user.first_name+" " + user.last_name, course_id.title, date_text, certificate.id)
    
    context = {
        'courses': courses,
        'course': course,
        'category': category,
        'time_duration': time_duration,
        'check_enroll': check_enroll,
        'comments': comments,
        'quizzes': quizzes,
        'result': result,
        'user': user,
        'certificate': certificate,
        'certificate_file': '/Media/certificate/certificate_template.jpg',
    }
    if action == 'comment':
        print("REQUEST")
        print(request)
        if request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('content')
            # course = request.POST.get('courseTitle')
            print(title, content, course)
            commented = Comment(
                user=request.user,
                course_review=title,
                comment=content,
                course=course
            )
            commented.save()
            messages.success(request, 'Comment successfully')

    return candy.render(request, 'course/course_details.html', context)

def PAGE_NOT_FOUND(request):
    return render(request, 'error/404.html')

@login_required
def SUCCESS(request):
    payment = Payment.objects.all()
    context = {
        'payment': payment
    }
    return candy.render(request, 'checkout/order_completed.html', context)

@login_required
def CHECKOUT(request, slug):
    course = Course.objects.get(slug=slug)
    category = Categories.get_all_category(Categories)
    action = request.GET.get('action')
    if course.price == 0:
        course = UserCourse(
            user=request.user,
            course=course
        )
        course.save()
        messages.success(request, 'Enrolled Successfully!')
        return candy.redirect('my-course')
    elif action == 'create_payment':
        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            country = request.POST.get('country')
            address_1 = request.POST.get('address_1')
            address_2 = request.POST.get('address_2')
            city = request.POST.get('city')
            state = request.POST.get('state')
            postcode = request.POST.get('postcode')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            order_comments = request.POST.get('order_comments')

            amount = course.price * 100
            currency = 'USD'
            notes = {
                'name': f'{first_name} {last_name}',
                'country': country,
                'address': f'{address_1} {address_2}',
                'city': city,
                'state': state,
                'postcode': postcode,
                'phone': phone,
                'email': email,
                'order_comments': order_comments,
                'category': category,
            }
            print(notes)
            receipt = f'Course-{int(time())}'
            payment = Payment(
                course=course,
                user=request.user,
                order_id=np.random.randint(100000, 999999)
            )
            payment.save()

            course = UserCourse(
                user=request.user,
                course=course
            )
            course.save()
            messages.success(request, 'Enrolled Successfully!')
            return candy.redirect('success')

    context = {
        'course': course,
    }
    return render(request, 'checkout/checkout.html', context)

@login_required
def MY_COURSE(request):
    category = Categories.get_all_category(Categories)
    course = UserCourse.objects.filter(user=request.user)

    context = {
        'course': course,
        'category': category,
    }
    return candy.render(request, 'course/my-course.html', context)

def MODAL(request):
    role = UserRole.objects.filter(user=request.user)

    context = {
        'role': role,
    }
    return render(request, 'course/modals.html', context)

@login_required
def WATCH_COURSE(request, slug):
    course = Course.objects.filter(slug=slug)
    lecture = request.GET.get('lecture')
    notes = Note.objects.filter(user=request.user)
    result = Result.objects.all()
    video = None
    if lecture:
        video = Video.objects.get(id=lecture)
    if course.exists():
        course = course.first()
    else:
        return redirect('404')

    user = request.user
    if user.id == None:
        check_enroll = None
    else:
        try:
            check_enroll = UserCourse.objects.get(
                user=request.user, course=course)
        except UserCourse.DoesNotExist:
            check_enroll = None

    context = {
        'course': course,
        'video': video,
        'check_enroll': check_enroll,
        'result': result,
        'notes': notes,
        'totalNotes': notes.count()
    }
    return render(request, 'course/watch-course.html', context)

@login_required
def QUIZ(request, course_slug, quizz_slug):
    category = Categories.get_all_category(Categories)
    course = Course.objects.filter(slug=course_slug)
    if course.exists():
        course = course.first()
    else:
        return redirect('404')
    quiz = Quizzes.objects.get(slug=quizz_slug)
    print("MY QUIZ: ", quiz)
    course_id = Course.objects.get(slug=course_slug)
    context = {
        'course': course_id,
        'quiz': quiz,
        'category': category,
    }
    try:
        if (quiz.result_set.get(quiz=quiz).attempt < quiz.total_attempts):
            user = quiz.result_set.get(quiz=quiz).user
            attempts =  quiz.result_set.get(quiz=quiz).attempt+1
            Result.objects.filter(quiz=quiz, user=user, course= course).update(attempt=attempts)
            quiz_data_view(request, course_slug, quizz_slug)
            return candy.render(request, 'quizzes/quizz_detail.html', context)
        else:
            return redirect('home')
    except:
        print("AAAAAAAAAAAAAAAAAAAAAAAA")
    quiz_data_view(request, course_slug, quizz_slug)
    return candy.render(request, 'quizzes/quizz_detail.html', context)
    
@login_required
def quiz_data_view(request, course_slug, quizz_slug):
    course = Course.objects.filter(slug=course_slug)
    if course.exists():
        course = course.first()
    else:
        return redirect('404')
    quiz = Quizzes.objects.get(slug=quizz_slug)
    questions = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({str(q): answers})
    return JsonResponse({'data': questions,
                         'time': quiz.time_duration})

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

@login_required
def save_quiz_view(request, course_slug, quizz_slug):
    course = Course.objects.get(slug=course_slug)
    if is_ajax(request):

        questions = []
        data = request.POST
        print("DATA: ",data)
        data_ = dict(data.lists())
        print("DATA_: ", data_)
        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            question = Question.objects.get(text=k)
            questions.append(question)

        user = request.user
        quiz = Quizzes.objects.get(slug=quizz_slug)

        score = 0
        results = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.text)
            
            if a_selected != "":
                question_answers = Answer.objects.filter(question=q).order_by("?")
                for a in question_answers:
                    if a_selected == a.text:
                        if a.correct:
                            score += q.point
                            correct_answer = a.text
                    else:
                        if a.correct:
                            correct_answer = a.text

                results.append(
                    {str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
            else:
                results.append({str(q): {'not_answered': None}})
        if score >= (quiz.require_passing_score):
            passed = True
        else:
            passed = False

        already_done = False
        add_new = False
        attempt = 0
        try:
            a = Result.objects.get(quiz=quiz, user=user, course=course)
            attempt = a.attempt
            already_done = True
            if a.score <= score:
                add_new = True
            else:
                add_new = False
        except:
            attempt = 1
            pass

        if add_new == True and already_done == True:
            a.delete()
            Result.objects.create(quiz=quiz, user=user,
                                  score=score, course=course, passed=passed, attempt=attempt)

        if already_done == False:
            Result.objects.create(quiz=quiz, user=user,
                                  score=score, course=course, passed=passed, attempt=attempt)

        if score >= quiz.require_passing_score:
            return JsonResponse({'passed': True, 'score': score, 'results': results}, safe=False)
        else:
            return JsonResponse({'passed': False, 'score': score, 'results': results}, safe=False)

@login_required
def INSTRUCTOR_SITE(request):
    if str(request.user) == "AnonymousUser":
        return candy.render(request, 'registration/login.html')
    else:
        # myUser = EmailBackEnd.authenticate( request,
        #                                     username=request.user.email,
        #                                     password=request.user.password)
        myRole = UserRole.objects.filter(user=request.user)
        if str(myRole[0]) == '0':
            messages.error(
                request, 'You do not have the permission to access this site !')
            return redirect('login')
        else:
            courses = Course.objects.all().filter(user=request.user)
            pendingCourses = Course.objects.all().filter(status="DRAFT", user=request.user)
           
            lessons = []
            lessonsCount = 0
            for course in courses:
                lesson = Lesson.objects.all().filter(course= course)
                lessons.append(lesson)

            for lesson in lessons:
                lessonsCount = lessonsCount+ lesson.count()

            pendingLessons = []
            plessonsCount = 0
            for course in pendingCourses:
                lesson = Lesson.objects.all().filter(course= course, status=False)
                pendingLessons.append(lesson)

            for lesson in pendingLessons:
                plessonsCount = plessonsCount+ lesson.count()
            
            quizzes = []
            quizzesCount = 0
            for course in courses:
                quiz = Quizzes.objects.all().filter(course= course)
                quizzes.append(quiz)

            for quiz in quizzes:
                quizzesCount = quizzesCount + quiz.count()
            pendingQuizzes = Quizzes.objects.all().filter(status=False)


            videos = []
            videosCount = 0
            for course in courses:
                video = Video.objects.all().filter(course= course)
                videos.append(video)

            for video in videos:
                videosCount = videosCount + video.count()
            pendingVideos = Video.objects.all().filter(status=False)

            context = {
                'courses': courses,
                'pendingCourses': pendingCourses,
                'lessons': lessons,
                'plessonsCount': plessonsCount,
                'quizzes': quizzes,
                'pendingQuizzes': pendingQuizzes,
                'videos': videos,
                'pendingVideos': pendingVideos,
                'lessonsCount': lessonsCount,
                'quizzesCount': quizzesCount,
                'videosCount': videosCount
            }
            return candy.render(request, 'instructor/instructor_dashboard.html', context=context)

@login_required
def INSTRUCTOR_COURSE(request):
    courses = Course.objects.all().filter(user=request.user)
    categories = Categories.objects.all()
    levels = Level.objects.all()
    context = {
        'courses': courses,
        'categories': categories,
        'levels': levels
    }
    print("COURSES: ", courses)
    print("LEVELS: ", levels)
    return candy.render(request, 'instructor/course.html', context=context)

@login_required
def INSTRUCTOR_LESSON(request):
    courses = Course.objects.all().filter(user=request.user)
    lessons = []
    for course in courses:
        lesson = Lesson.objects.all().filter(course= course)
        lessons.append(lesson)
    context = {
        'lessons': lessons
    }
    return candy.render(request, 'instructor/lesson.html', context=context)

@login_required
def INSTRUCTOR_VIDEO(request):
    courses = Course.objects.all().filter(user=request.user)
    videos = []
    for course in courses:
        video = Video.objects.all().filter(course= course)
        videos.append(video)
 
    context = {
        'videos': videos
    }
    return candy.render(request, 'instructor/video.html', context=context)

@login_required
def INSTRUCTOR_QUIZZ(request):
    courses = Course.objects.all().filter(user=request.user)
    quizzes = []
    for course in courses:
        quiz = Quizzes.objects.all().filter(course= course)
        quizzes.append(quiz)
    context = {
        'quizzes': quizzes
    }
    print("QUIZZES: ",quizzes)
    return candy.render(request, 'instructor/quizz.html', context=context)

@login_required
def INSTRUCTOR_PROFILE(request):
    instructor = Instructor.objects.filter(user=request.user).get()
    email = request.user.email
    cv = str(instructor.cv).split('/')[-1]
    context = {
        'instructor': instructor,
        'email': email,
        "cv": cv
    }
    return candy.render(request, 'instructor/instructor_profile.html', context=context)

@login_required
def InstructorCreateCourse(request):
    createCourseForm = InstructorCreateCourseForm()
    author = User.objects.get(username=request.user)
    message = None
    mydict = {'createCourseForm': createCourseForm,
              'author': author, 'message': message}
    
    if request.method == 'POST':
        createCourseForm = InstructorCreateCourseForm(request.POST, request.FILES)
        if createCourseForm.is_valid():
            newCourse=createCourseForm.save(commit=False) 
            newCourse.user = author
            newCourse.level = Level.objects.get(name=request.POST.get('level'))
            newCourse.category = Categories.objects.get(name=request.POST.get('category'))
            newCourse.language = Language.objects.get(id=request.POST.get('language'))
            newCourse.status = 'DRAFT'
            newCourse.save()
            return redirect('instructor-course')
        else:
            print(createCourseForm.errors)

    else:  # no POST yet
        createCourseForm = InstructorCreateCourseForm()
    return render(request, 'instructor/create_course_form.html', context=mydict)

@login_required
def InstructorCreateLesson(request):
    createLessonForm = InstructorCreateLessonForm()
    author = User.objects.get(username=request.user)
    message = None
    mydict = {'createLessonForm': createLessonForm,
              'author': author, 'message': message}
    
    if request.method == 'POST':
        createLessonForm = InstructorCreateLessonForm(request.POST)
        if createLessonForm.is_valid():
            newLesson=createLessonForm.save(commit=False) 
            newLesson.course = Course.objects.get(id=request.POST.get('course'))
            newLesson.status = False
            newLesson.save()
            return redirect('instructor-lesson')
        else:
            print(createLessonForm.errors)

    else:  # no POST yet
        createLessonForm = InstructorCreateLessonForm()
    return render(request, 'instructor/create_lesson_form.html', context=mydict)

@login_required
def InstructorCreateQuiz(request):
    createQuizForm = InstructorCreateQuizzForm()
    author = User.objects.get(username=request.user)
    message = None
    mydict = {'createQuizForm': createQuizForm,
              'author': author, 'message': message}
    
    if request.method == 'POST':
        createQuizForm = InstructorCreateQuizzForm(request.POST)
        if createQuizForm.is_valid():
            # print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
            newQuiz=createQuizForm.save(commit=False) 
            newQuiz.course = Course.objects.get(id=request.POST.get('course'))
            newQuiz.lesson = Lesson.objects.get(id=request.POST.get('lesson'))
            newQuiz.status = False
            newQuiz.save()
            return redirect('instructor-quiz')
        else:
            print(createQuizForm.errors)

    else:  # no POST yet
        # print("KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
        createQuizForm = InstructorCreateQuizzForm()
    return render(request, 'instructor/create_quiz_form.html', context=mydict)

@login_required
def InstructorCreateVideo(request):
    createVideoForm = InstructorCreateVideoForm()
    author = User.objects.get(username=request.user)
    message = None
    mydict = {'createVideoForm': createVideoForm,
              'author': author, 'message': message}
    
    if request.method == 'POST':
        createVideoForm = InstructorCreateVideoForm(request.POST)
        if createVideoForm.is_valid():
            newVideo=createVideoForm.save(commit=False) 
            newVideo.course = Course.objects.get(id=request.POST.get('course'))
            newVideo.lesson = Lesson.objects.get(name=request.POST.get('lesson'))
            newVideo.status = False
            newVideo.save()
            return redirect('instructor-video')
        else:
            print(createVideoForm.errors)

    else:  # no POST yet
        createVideoForm = InstructorCreateVideoForm()
    return render(request, 'instructor/create_video_form.html', context=mydict)

@login_required
def VIDEO_LECTURE_DETAILS(request, slug):
    video = Video.objects.get(youtube_id=slug)

    context = {
        'video': video,
    }

    return render(request, 'instructor/update_video_form.html', context)

@login_required
def INSTRUCTOR_COURSE_DETAILS(request, slug):
    course = Course.objects.get(slug=slug)

    context = {
        'course': course,
    }

    return render(request, 'instructor/upload_course_forn.html', context)

def UPDATE_INSTRUCTOR_PROFILE(request):
    first_name = request.POST().get('fname')
    last_name = request.POST().get('lname')
    phone = request.POST().get('phone')
    gender = request.POST().get('gender')
    cv = request.POST().get('cv')
    user_id = request.user.id

    instructor = Instructor.objects.get(id = user_id)
    instructor.First_Name = first_name
    instructor.Last_Name = last_name
    instructor.phone = phone
    instructor.gender = gender
    instructor.cv = cv

    instructor.save()
    messages.success(request, 'Profile Are Successfully Updated.')
    return render(request, 'instructor/instructor_profile.html')

def INSTRUCTOR_CHANGE_PASSWORD(request):
    instructor = User.objects.filter(username=request.user).get()
    password = instructor.password
  
    context = {
        'password': password,
    }
    return candy.render(request, 'instructor/instructor_change_password.html', context=context)

def EDIT_NOTE(request):
    noteId = request.POST.get("noteId")
    if request.method == "POST":
        note = request.POST.get("note")
        Note.objects.filter(id=int(noteId)).update(body=note)
        Note.objects.filter(id=1).delete
    #     print("AAAAAAAAA", note)
    return redirect('home')

def CREATE_NOTE(request):
    # noteId = request.POST.get("noteId")
    if request.method == "POST":
        note = request.POST.get("note")
        Note.objects.create(user=request.user, body=note)
    return redirect('home')