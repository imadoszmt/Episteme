from django.db import models
from django.contrib.auth.models import User

class Quiz(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    duration = models.CharField(max_length=50, default='1 hour')  # e.g., "1 hour", "30 mins"
    is_free = models.BooleanField(default=True)
    is_friendly = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def get_next_question(self, current_question):
        return self.questions.filter(id__gt=current_question.id).first()
    
    def get_previous_question(self, current_question):
        return self.questions.filter(id__lt=current_question.id).last()
    
    def get_question_number(self, current_question):
        return list(self.questions.all()).index(current_question) + 1
    
    def get_progress(self, current_question):
        question_number = self.get_question_number(current_question)
        total_questions = self.questions.count()
        return (question_number / total_questions) * 100
    
    def is_last_question(self, current_question):
        return not self.questions.filter(id__gt=current_question.id).exists()

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(upload_to='question_images/', null=True, blank=True)
    explanation = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.quiz.title} - Question {self.id}"
    
    @property
    def correct_option(self):
        return self.options.filter(is_correct=True).first()

class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return self.text

class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s answer to {self.question}"
    
    def is_correct(self):
        return self.selected_option.is_correct
