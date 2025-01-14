from .models import Quiz
def get_quiz_questions(quiz_type):
    quiz = Quiz.objects.get(quiz_type=quiz_type)
    questions = []
    
    for question in quiz.questions.all():
        question_data = {
            'text': question.question_text,
            'options': [option.text for option in question.options.all()],
            'correct_answer': next(
                (option.text for option in question.options.all() if option.is_correct),
                None
            )
        }
        questions.append(question_data)
    
    return questions