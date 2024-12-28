from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'quiz'

urlpatterns = [
    path('', views.home, name='home'),
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('quiz/<int:quiz_id>/question/<int:question_id>/', views.quiz_question, name='quiz_question'),
    path('quiz/<int:quiz_id>/results/', views.quiz_results, name='quiz_results'),
    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('login/', TemplateView.as_view(template_name='account/login.html'), name='login'),
    path('signup/', TemplateView.as_view(template_name='account/signup.html'), name='signup'),
] 