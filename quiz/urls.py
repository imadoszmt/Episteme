from django.urls import path
from .views import (
    signup,
    login_view,
    account_profile,
    quiz_list,
    quiz_detail,
    quiz_question,
    quiz_results,
    logout_view,
    home,
    networking_quiz,
)

app_name = 'quiz'

urlpatterns = [
    path('', home, name='home'),
    path('quizzes/', quiz_list, name='quiz_list'),  
    path('signup/', signup, name='account_signup'),
    path('login/', login_view, name='account_login'),
    path('profile/', account_profile, name='account_profile'),
    path('logout/', logout_view, name='logout'),
    path('quiz/<int:quiz_id>/', quiz_detail, name='quiz_detail'),
    path('quiz/<int:quiz_id>/question/<int:question_id>/', quiz_question, name='quiz_question'),
    path('quiz/<int:quiz_id>/results/', quiz_results, name='quiz_results'),
    path('quizzes/networking/', networking_quiz, name='networking_quiz'),
] 