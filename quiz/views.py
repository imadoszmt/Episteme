import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Quiz, Question, UserAnswer, Option, QuizAttempt
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import redirect
from django.db.models import Prefetch, Count, Avg, Max
from django.http import JsonResponse
from .utils import get_quiz_questions

def home(request):
    # Get the most taken quizzes (top 3)
    featured_quizzes = Quiz.objects.annotate(
        attempt_count=Count('attempts')
    ).order_by('-attempt_count')[:3]
    
    context = {
        'featured_quizzes': featured_quizzes
    }
    return render(request, 'home.html', context)

# Custom logout view
def direct_logout(request):
    logout(request)
    return redirect('/')  # Redirect to homepage or desired URL

@login_required
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    context = {
        'quiz': quiz,
    }
    return render(request, 'quiz/quiz_detail.html', context)

@login_required
def quiz_question(request, quiz_id, question_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = []
    
    # Format all questions for the quiz
    for question in quiz.questions.all():
        question_data = {
            'id': question.id,
            'text': question.question_text,
            'options': [],
            'correct_answer': ''
        }
        
        for option in question.options.all():
            question_data['options'].append(option.text)
            if option.is_correct:
                question_data['correct_answer'] = option.text
        
        questions.append(question_data)
    
    context = {
        'quiz': quiz,
        'questions': json.dumps(questions),
        'total_questions': len(questions)
    }
    
    # Handle answer submission
    if request.method == 'POST':
        data = json.loads(request.body)
        answers = data.get('answers', {})
        
        quiz_attempt = QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            score=0
        )
        
        correct_answers = 0
        total_questions = len(questions)
        
        for question_id, answer in answers.items():
            question = get_object_or_404(Question, id=question_id)
            selected_option = get_object_or_404(Option, question=question, text=answer)
            
            UserAnswer.objects.create(
                quiz_attempt=quiz_attempt,
                user=request.user,
                quiz=quiz,
                question=question,
                selected_option=selected_option
            )
            
            if selected_option.is_correct:
                correct_answers += 1
        
        # Calculate and save score
        score = (correct_answers / total_questions) * 100
        quiz_attempt.score = round(score)
        quiz_attempt.save()
        
        return JsonResponse({
            'success': True,
            'score': quiz_attempt.score,
            'redirect_url': reverse('quiz:quiz_results', args=[quiz_attempt.id])
        })
    
    return render(request, 'quiz/quiz.html', context)

@login_required
def quiz_results(request, attempt_id):
    quiz_attempt = get_object_or_404(QuizAttempt.objects.select_related('quiz'), id=attempt_id)
    
    # Ensure user can only view their own results
    if quiz_attempt.user != request.user:
        return redirect('home')
    
    user_answers = quiz_attempt.answers.all().select_related(
        'question',
        'selected_option'
    )
    
    context = {
        'quiz_attempt': quiz_attempt,
        'score': quiz_attempt.score,
        'user_answers': user_answers,
        'total_questions': user_answers.count(),
        'correct_answers': sum(1 for answer in user_answers if answer.selected_option.is_correct)
    }
    
    return render(request, 'results.html', context)

def quiz_list(request):
    quizzes = Quiz.objects.all().order_by('-created_at')
    return render(request, 'quiz/quiz_list.html', {'quizzes': quizzes})

@login_required
def profile_view(request):
    # Get user's quiz attempts with aggregated data
    quiz_attempts = QuizAttempt.objects.filter(user=request.user)\
        .select_related('quiz')\
        .order_by('-created_at')
    
    # Get statistics for the user
    stats = {
        'total_quizzes': quiz_attempts.count(),
        'average_score': quiz_attempts.aggregate(Avg('score'))['score__avg'] or 0,
        'best_score': quiz_attempts.aggregate(Max('score'))['score__max'] or 0,
        'total_time': quiz_attempts.count() * 30  # Assuming each quiz takes 30 minutes
    }
    
    context = {
        'quiz_attempts': quiz_attempts,
        'user': request.user,
        'stats': stats
    }
    return render(request, 'account/profile.html', context)

@login_required
def submit_quiz(request, quiz_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    quiz = get_object_or_404(Quiz, id=quiz_id)
    answers_data = request.POST.get('answers', None)
    
    if not answers_data:
        return JsonResponse({'error': 'No answers provided'}, status=400)
    
    try:
        answers = json.loads(answers_data)
        total_questions = quiz.questions.count()
        correct_answers = 0
        
        # Create quiz attempt
        quiz_attempt = QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            score=0  # Will be updated after calculating
        )
        
        # Process each answer
        for question_id, option_id in answers.items():
            question = Question.objects.get(id=question_id)
            selected_option = Option.objects.get(id=option_id)
            
            # Save user's answer
            UserAnswer.objects.create(
                quiz_attempt=quiz_attempt,
                question=question,
                selected_option=selected_option
            )
            
            # Count correct answers
            if selected_option.is_correct:
                correct_answers += 1
        
        # Calculate and update score
        score = (correct_answers / total_questions) * 100
        quiz_attempt.score = round(score)
        quiz_attempt.save()
        
        return JsonResponse({
            'success': True,
            'score': quiz_attempt.score,
            'redirect_url': reverse('quiz_results', args=[quiz_attempt.id])
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    

@login_required
def web_programming_quiz(request):
    questions = get_quiz_questions('web_programming')
    return render(request, 'quiz/web_programming_quiz.html', {'questions': questions})

@login_required
def database_quiz(request):
    questions = get_quiz_questions('database')
    return render(request, 'quiz/database_quiz.html', {'questions': questions})

@login_required
def python_quiz(request):
    questions = get_quiz_questions('python')
    return render(request, 'quiz/python_quiz.html', {'questions': questions})

@login_required
def javascript_quiz(request):
    questions = get_quiz_questions('javascript')
    return render(request, 'quiz/javascript_quiz.html', {'questions': questions})

@login_required
def c_programming_quiz(request):
    questions = get_quiz_questions('c_programming')
    return render(request, 'quiz/c_programming_quiz.html', {'questions': questions})

@login_required
def networking_quiz(request):
    questions = get_quiz_questions('networking')
    return render(request, 'quiz/networking_quiz.html', {'questions': questions})

@login_required
def delete_quiz_attempt(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
    attempt.delete()
    messages.success(request, 'Quiz attempt deleted successfully.')
    return redirect('quiz:profile_view')