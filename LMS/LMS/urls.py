from django.contrib import admin
from django.urls import path, include
from .import views, user_login
from django.conf import settings
from django.conf.urls.static import static
from . import candy

urlpatterns = [
    path('admin/', admin.site.urls),

    *candy.path('base', views.BASE,name='base'),

    path('404', views.PAGE_NOT_FOUND, name='404'),

    *candy.path('', views.HOME,name='home'),

    # path('notes/', views.getNotes, name="notes"),

    # path('notes/<str:pk>/', views.getNote, name="note"),

    path('courses', views.SINGLE_COURSE,name='single_course'),

    *candy.path('courses/filter-data',views.filter_data,name="filter-data"),

    *candy.path('course/<slug:slug>',views.COURSE_DETAILS,name='course_details'),   

    path('search',views.SEARCH_COURSE,name='search_course'),

    *candy.path('contact', views.CONTACT_US,name='contact_us'),

    *candy.path('about', views.ABOUT_US,name='about_us'),

    *candy.path('become-an-instructor', views.BECOME_AN_INSTRUCTOR,name='become_an_instructor'),

    *candy.path('coming_soon', views.COMING_SOON,name='coming_soon'),

     *candy.path('success', views.SUCCESS,name='success'),

    path('event', views.EVENT,name='event'),

    *candy.path('accounts/register', user_login.REGISTER, name='register'),
    *candy.path('accounts/learner-register', user_login.LEARNER_SIGNUP, name='learner_register'),
    *candy.path('accounts/instructor-register', user_login.INSTRUCTOR_SIGNUP, name='instructor_register'),

    path('accounts/', include('django.contrib.auth.urls')),

    *candy.path('doLogin', user_login.DO_LOGIN, name='doLogin'),

    # path('patientsignup/', views.LearnerSignUp, name="patientsignup"),

    # path('patientsignup/', views.InstructorSi, name="patientsignup"),

    path('accounts/profile', user_login.PROFILE, name='profile'),

    path('accounts/profile/update', user_login.PROFILE_UPDATE, name='profile_update'),

    *candy.path('checkout/<slug:slug>',views.CHECKOUT,name='checkout'),

    *candy.path('my-course',views.MY_COURSE,name='my-course'),

    path('course/watch-course/<slug:slug>',views.WATCH_COURSE,name='watch-course'),

    *candy.path('course/<slug:course_slug>/<slug:quizz_slug>',views.QUIZ,name='quiz'),

    path('course/<slug:course_slug>/<slug:quizz_slug>/data', views.quiz_data_view, name='quiz-data-view'),

    path('course/<slug:course_slug>/<slug:quizz_slug>/save',
         views.save_quiz_view, name='save_quiz_view'),

    path('blog', views.BLOG, name='blog'),

    #NOTE_CRUD
    # *candy.path('delete_note/<slug:slug>', views.InstructorCreateCourse, name="delete_note"),

    #INSTRUCTOR
    *candy.path('instructor-dashboard', views.INSTRUCTOR_SITE, name='instructor-dashboard'),
    *candy.path('instructor-course', views.INSTRUCTOR_COURSE, name='instructor-course'),
    *candy.path('instructor-lesson', views.INSTRUCTOR_LESSON, name='instructor-lesson'),
    *candy.path('instructor-video', views.INSTRUCTOR_VIDEO, name='instructor-video'),
    *candy.path('instructor-quiz', views.INSTRUCTOR_QUIZZ, name='instructor-quiz'),
    *candy.path('instructor-profile', views.INSTRUCTOR_PROFILE, name="instructor-profile"),
    *candy.path('instructor-change-password', views.INSTRUCTOR_CHANGE_PASSWORD, name="instructor-change-password"),

    # *candy.path('instructor-create-course', views.CreateCourseForm, name='instructor-create-course'),
    *candy.path('create_course_form', views.InstructorCreateCourse, name="create_course_form"),
    *candy.path('create_lesson_form', views.InstructorCreateLesson, name="create_lesson_form"),
    *candy.path('create_quiz_form', views.InstructorCreateQuiz, name="create_quiz_form"),
    *candy.path('create_video_form', views.InstructorCreateVideo, name="create_video_form"),
    *candy.path('video-lecture/details/<slug:slug>/',views.VIDEO_LECTURE_DETAILS,name='video_lecture_details'),
    *candy.path('instructor-course/details/<slug:slug>/',views.INSTRUCTOR_COURSE_DETAILS,name='instructor_course_details'),

    path('instructor/search/course',views.INSTRUCTOR_SEARCH_COURSE,name='instructor_search_course'),
    path('instructor/search/lesson',views.INSTRUCTOR_SEARCH_LESSON,name='instructor_search_lesson'),
    path('instructor/search/quiz',views.INSTRUCTOR_SEARCH_QUIZZ,name='instructor_search_quiz'),
    path('instructor/search/video-lecture',views.INSTRUCTOR_SEARCH_VIDEO_LECTURE,name='instructor_search_video_lecture'),

    path('edit-note',views.EDIT_NOTE,name='edit_note'),
    path('create-note',views.CREATE_NOTE,name='create_note'),


] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
