from django.core.management.base import BaseCommand
from quiz.views import create_quizzes

class Command(BaseCommand):
    help = 'Creates initial quiz data'

    def handle(self, *args, **kwargs):
        create_quizzes()
        self.stdout.write(self.style.SUCCESS('Successfully created quizzes'))
