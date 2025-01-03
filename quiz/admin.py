from django.contrib import admin
from .models import Quiz, Question, Option, UserAnswer

class OptionInline(admin.TabularInline):
    model = Option
    extra = 4

class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionInline]
    list_display = ('quiz', 'question_text', 'created_at')
    list_filter = ('quiz', 'created_at')
    search_fields = ('question_text', 'quiz__title')

class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'description')

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(UserAnswer)
