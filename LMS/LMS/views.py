from time import time
import numpy as np
from django.shortcuts import redirect, render
from app.models import *
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Sum
from django.contrib import messages

from .settings import *
import razorpay

# client = razorpay.Client(auth=(KEY_ID,KEY_SECRET))

def BASE(request):
    return render(request, 'base.html')

def HOME(request):
    category = Categories.objects.all().order_by('id')[0:5]
    course = Course.objects.filter(status = 'PUBLISH').order_by('-id')
    user = request.user
    context = {
        'category':category,
        'course':course,
        'user':user,
    }
    return render(request, 'Main/home.html', context)

def SINGLE_COURSE(request):
    category = Categories.get_all_category(Categories)
    level = Level.objects.all()
    course = Course.objects.all()
    context = {
        'category':category,
        'level':level,
        'course':course,
    }
    return render(request, 'Main/single_course.html', context)

def CONTACT_US(request):
    category = Categories.objects.all().order_by('id')[0:5]
    course = Course.objects.filter(status='PUBLISH').order_by('-id')

    context = {
        'category': category,
        'course': course,
    }
    return render(request, 'Main/contact_us.html', context)

def ABOUT_US(request):
    category = Categories.objects.all().order_by('id')[0:5]
    course = Course.objects.filter(status='PUBLISH').order_by('-id')

    context = {
        'category': category,
        'course': course,
    }
    return render(request, 'Main/about_us.html', context)

def filter_data(request):
    categories = request.GET.getlist('category[]')
    level = request.GET.getlist('level[]')
    if categories:
       course = Course.objects.filter(category__id__in=categories).order_by('-id')
    elif level:
       course = Course.objects.filter(level__id__in = level).order_by('-id')
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
    course = Course.objects.filter(title__icontains = query)
    context = {
        'course':course,
        'category': category,
    }
    return render(request,'search/search.html', context)

def COURSE_DETAILS(request, slug):
    courses = Course.objects.all()
    category = Categories.get_all_category(Categories)
    time_duration = Video.objects.filter(course__slug = slug).aggregate(sum=Sum('time_duration'))
    course_id = Course.objects.get(slug=slug)
    comments = Comment.objects.all()
    quizzes = Quizzes.objects.filter(course = course_id)
    result = None
    try :
        result = Result.objects.filter(user=request.user)
    except:
        pass
    user = request.user
    if user.id == None:
        check_enroll = None
    else:
        try :
            check_enroll = UserCourse.objects.get(user=request.user,course=course_id)
        except UserCourse.DoesNotExist:
            check_enroll = None

    course = Course.objects.filter(slug=slug)
    if course.exists():
        course = course.first()
    else:
        return redirect('404')
    action = request.GET.get('action')

    context = {
        'courses': courses,
        'course':course,
        'category':category,
        'time_duration':time_duration,
        'check_enroll':check_enroll,
        'user':user,
        'comments':comments,
        'quizzes':quizzes,
        'result':result,
        'user':user,
    }
    if action == 'comment':
        if request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('content')
            print(title, content)
            commented = Comment(
                user = request.user,
                course_review = title,
                comment = content,
            )
            commented.save()
            messages.success(request, 'Comment successfully')

    return render(request,'course/course_details.html', context)

def PAGE_NOT_FOUND(request):
    return render(request, 'error/404.html')

def CHECKOUT(request,slug):
    course = Course.objects.get(slug = slug)
    category = Categories.get_all_category(Categories)
    action = request.GET.get('action')
    if course.price == 0:
        course = UserCourse(
            user = request.user,
            course = course
        )
        course.save()
        messages.success(request,'Enrolled Successfully!')
        return redirect('my-course')
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
                order_id= np.random.randint(100000,999999)
            )
            payment.save()

            course = UserCourse(
                user=request.user,
                course=course
            )
            course.save()
            messages.success(request, 'Enrolled Successfully!')
            return redirect('my-course')

    context = {
        'course':course,
    }
    return render(request, 'checkout/checkout.html', context)

def MY_COURSE(request):
    category = Categories.get_all_category(Categories)
    course = UserCourse.objects.filter(user = request.user)

    context = {
        'course':course,
        'category': category,
    }
    return render(request, 'course/my-course.html',context)


def WATCH_COURSE(request, slug):
    course = Course.objects.filter(slug =slug)
    lecture = request.GET.get('lecture')
    video = None
    if lecture:
        video = Video.objects.get(id=lecture)

    if  course.exists():
        course = course.first()
    else:
        return redirect('404')
    context = {
        'course':course,
        'video':video,
        
    }
    return render(request,'course/watch-course.html',context)

def QUIZ(request, course_slug, quizz_slug): 
    category = Categories.get_all_category(Categories)
    course = Course.objects.filter(slug=course_slug)
    if course.exists():
        course = course.first()
    else:
        return redirect('404')
    quiz = Quizzes.objects.get(slug=quizz_slug)
    course_id = Course.objects.get(slug=course_slug)
    context = {
        'course': course_id,
        'quiz': quiz,
        'category': category,
    }
    quiz_data_view(request, course_slug, quizz_slug)
    return render(request, 'quizzes/quizz_detail.html', context)

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

def save_quiz_view(request, course_slug, quizz_slug):
    course = Course.objects.get(slug=course_slug)
    if is_ajax(request):
        questions = []
        data = request.POST
        data_ = dict(data.lists())

        data_.pop('csrfmiddlewaretoken')
        
        for k in data_.keys():
            print(k)
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
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:
                    if a_selected == a.text:
                        if a.correct:
                            score += q.point
                            correct_answer = a.text
                    else:
                        if a.correct:
                            correct_answer = a.text

                results.append({str(q): {'correct_answer': correct_answer,'answered': a_selected}})
            else:
                results.append({str(q): {'not answered'}})
        
        if score >= quiz.require_passing_score:
            passed = True
        else:
            passed = False

        already_done = False            
        add_new = False

        try :
            a = Result.objects.get(quiz=quiz, user=user, course=course)
            already_done = True
            if a.score <= score:
                add_new = True
            else:
                add_new = False
        except:
            pass
        
        if add_new == True and already_done == True:
            a.delete()
            Result.objects.create(quiz=quiz, user=user,
                                    score=score, course=course, passed=passed)
            
        if already_done == False:
            Result.objects.create(quiz=quiz, user=user,
                                    score=score, course=course, passed=passed)

        if score > quiz.require_passing_score:
            return JsonResponse({'passed': True, 'score': score, 'results': results})
        else:
            return JsonResponse({'passed': False, 'score': score, 'results': results})
    