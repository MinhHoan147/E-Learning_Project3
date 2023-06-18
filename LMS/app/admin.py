from django.contrib import admin
from .models import *
# Register your models here.

class what_you_learn_TabularInline(admin.TabularInline):
    model = What_you_learn

class Requirements_TabularInline(admin.TabularInline):
    model = Requirements

class Video_TabularInline(admin.TabularInline):
    model = Video

class Lesson_TabularInline(admin.TabularInline):
    model = Lesson

class course_admin(admin.ModelAdmin):
    inlines = (what_you_learn_TabularInline, Requirements_TabularInline, Lesson_TabularInline, Video_TabularInline,)

class create_question(admin.TabularInline):
    model = Question

class quiz_admin(admin.ModelAdmin):
    inlines = (create_question,)

class create_answer(admin.TabularInline):
    model = Answer

class question_admin(admin.ModelAdmin):
    inlines = (create_answer,)

admin.site.register(Categories)
admin.site.register(Author)
admin.site.register(Course, course_admin)
admin.site.register(Comment)
admin.site.register(Level)
admin.site.register(Language)
admin.site.register(What_you_learn)
admin.site.register(Requirements)
admin.site.register(Lesson)
admin.site.register(UserCourse)
admin.site.register(Payment)
admin.site.register(Question, question_admin)
admin.site.register(Quizzes, quiz_admin)
admin.site.register(Result)
admin.site.register(Note)
admin.site.register(Role)
admin.site.register(UserRole)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Video)
admin.site.register(Watch_Duration)
admin.site.register(Certificate)
