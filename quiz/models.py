from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class Quiz(models.Model):
    LEVEL_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='easy')
    duration = models.IntegerField(help_text="Duration in minutes")
    is_free = models.BooleanField(default=True)
    is_friendly = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_next_question(self, current_question):
        # Logic to get the next question based on the current question
        questions = self.questions.all()
        current_index = list(questions).index(current_question)
        if current_index + 1 < len(questions):
            return questions[current_index + 1]
        return None

    def get_previous_question(self, current_question):
        # Logic to get the previous question based on the current question
        questions = self.questions.all()
        current_index = list(questions).index(current_question)
        if current_index - 1 >= 0:
            return questions[current_index - 1]
        return None

    def get_question_number(self, question):
        # Logic to get the question number
        questions = self.questions.all()
        return list(questions).index(question) + 1

    def get_progress(self, current_question):
        # Logic to calculate progress
        questions = self.questions.all()
        return (self.get_question_number(current_question) / questions.count()) * 100

    def is_last_question(self, question):
        # Logic to check if the question is the last one
        questions = self.questions.all()
        return list(questions).index(question) == len(questions) - 1

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Additional fields can be added here if needed

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    question_text = models.TextField()
    choices = models.JSONField(default=list)
    correct_answer = models.TextField()
    difficulty = models.TextField(default='easy')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_text

class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class QuizSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)

class Answer(models.Model):
    quiz_session = models.ForeignKey(QuizSession, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_response = models.TextField()
    is_correct = models.BooleanField()

class Leaderboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    achieved_at = models.DateTimeField(auto_now_add=True)

class Badge(models.Model):
    name = models.TextField()
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    awarded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, related_name='quiz_attempts', on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, related_name='attempts', on_delete=models.CASCADE)
    score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']  # Show most recent attempts first

    def __str__(self):
        return f"{self.user.username}'s attempt at {self.quiz.title}"


class UserAnswer(models.Model):
    quiz_attempt = models.ForeignKey(QuizAttempt, related_name='answers', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE)
    score = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Answer by {self.quiz_attempt.user.username} for {self.question}"
    
    def is_correct(self):
        return self.selected_option.is_correct
