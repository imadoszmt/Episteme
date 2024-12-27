from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.home, name='home'),
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('quiz/<int:quiz_id>/question/<int:question_id>/', views.quiz_question, name='quiz_question'),
    path('quiz/<int:quiz_id>/results/', views.quiz_results, name='quiz_results'),
] 