from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.home, name='home'),
    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('profile/', views.profile_view, name='profile_view'),
    path('accounts/logout/', views.direct_logout, name='account_logout'),
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('quiz/<int:quiz_id>/question/<int:question_id>/', views.quiz_question, name='quiz_question'),
    path('quiz/attempt/<int:attempt_id>/results/', views.quiz_results, name='quiz_results'),
    path('quizzes/networking/', views.networking_quiz, name='networking_quiz'),
    path('quizzes/webprogramming/', views.web_programming_quiz, name='web_programming_quiz'),
    path('quizzes/database/', views.database_quiz, name='database_quiz'),
    path('quizzes/python/', views.python_quiz, name='python_quiz'),
    path('quizzes/javascript/', views.javascript_quiz, name='javascript_quiz'),
    path('quizzes/cprogramming/', views.c_programming_quiz, name='c_programming_quiz'),
    path('quiz/<int:quiz_id>/start/', views.quiz_question, name='start_quiz'),
    path('quiz/attempt/<int:attempt_id>/delete/', views.delete_quiz_attempt, name='delete_quiz_attempt'),
]