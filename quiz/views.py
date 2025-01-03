from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, UserAnswer
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
import re

def home(request):
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')  # Redirect to home after logout

@login_required
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return render(request, 'quiz.html', {'quiz': quiz})

@login_required
def quiz_question(request, quiz_id, question_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    question = get_object_or_404(Question, id=question_id, quiz=quiz)
    
    if request.method == 'POST':
        selected_option = request.POST.get('answer')
        if selected_option:
            UserAnswer.objects.create(
                user=request.user,
                quiz=quiz,
                question=question,
                selected_option_id=selected_option
            )
            next_question = quiz.get_next_question(question)
            if next_question:
                return redirect('quiz_question', quiz_id=quiz.id, question_id=next_question.id)
            return redirect('quiz_results', quiz_id=quiz.id)
    
    context = {
        'quiz': quiz,
        'question': question,
        'current_question_no': quiz.get_question_number(question),
        'total_questions': quiz.questions.count(),
        'progress': quiz.get_progress(question),
        'prev_question': quiz.get_previous_question(question),
        'is_last_question': quiz.is_last_question(question)
    }
    return render(request, 'quiz.html', context)

@login_required
def quiz_results(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    user_answers = UserAnswer.objects.filter(user=request.user, quiz=quiz)
    
    correct_answers = sum(1 for answer in user_answers if answer.is_correct())
    total_questions = quiz.questions.count()
    score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
    
    context = {
        'quiz': quiz,
        'score': round(score, 1),
        'correct_answers': correct_answers,
        'total_questions': total_questions,
        'user_answers': user_answers
    }
    return render(request, 'results.html', context)

def quiz_list(request):
    quizzes = Quiz.objects.all().order_by('-created_at')
    return render(request, 'quiz/quiz_list.html', {'quizzes': quizzes})

@login_required
def account_profile(request):
    quiz_attempts = UserAnswer.objects.filter(user=request.user)  # Assuming UserAnswer tracks quiz attempts
    return render(request, 'account/profile.html', {'quiz_attempts': quiz_attempts})

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messages.error(request, 'Invalid email format.')
            return render(request, 'account/signup.html')

        # Validate username uniqueness
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'account/signup.html')

        # Validate password complexity
        if len(password1) < 8:  # Check for minimum length
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'account/signup.html')

        if not re.search(r"[A-Za-z]", password1):  # Check for letters
            messages.error(request, 'Password must contain at least one letter.')
            return render(request, 'account/signup.html')

        if not re.search(r"\d", password1):  # Check for numbers
            messages.error(request, 'Password must contain at least one number.')
            return render(request, 'account/signup.html')

        if password1.isdigit():  # Check if password is purely numeric
            messages.error(request, 'Password cannot be entirely numeric.')
            return render(request, 'account/signup.html')

        # Check if passwords match
        if password1 == password2:
            try:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                login(request, user)  # Log the user in after registration
                messages.success(request, 'Account created successfully! Redirecting to your profile...')
                return redirect('account_profile')  # Redirect to the profile page
            except Exception as e:
                messages.error(request, f'Error creating account: {e}')
        else:
            messages.error(request, 'Passwords do not match.')
    return render(request, 'account/signup.html')

def login_view(request):
    if request.method == 'POST':
        login_param = request.POST.get('login')  # This can be username or email
        password = request.POST.get('password')
        user = authenticate(request, username=login_param, password=password)
        if user is not None:
            login(request, user)
            return redirect('account_profile')  # Redirect to profile after login
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'account/login.html')

