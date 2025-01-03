from django.test import TestCase
from .models import Quiz, Question

class QuizModelTest(TestCase):
    def setUp(self):
        self.quiz = Quiz.objects.create(title='Sample Quiz', description='A test quiz.')

    def test_quiz_creation(self):
        self.assertEqual(self.quiz.title, 'Sample Quiz')
        self.assertEqual(self.quiz.description, 'A test quiz.')

class QuestionModelTest(TestCase):
    def setUp(self):
        self.quiz = Quiz.objects.create(title='Sample Quiz', description='A test quiz.')
        self.question = Question.objects.create(quiz=self.quiz, question_text='What is 2 + 2?', correct_answer='4')

    def test_question_creation(self):
        self.assertEqual(self.question.question_text, 'What is 2 + 2?')
        self.assertEqual(self.question.correct_answer, '4')
