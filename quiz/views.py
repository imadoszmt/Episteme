from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, UserAnswer

def home(request):
    return render(request, 'home.html')

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
