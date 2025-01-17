# Generated by Django 4.2.17 on 2025-01-02 18:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0002_quiz_duration_quiz_is_free_quiz_is_friendly_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='explanation',
        ),
        migrations.RemoveField(
            model_name='question',
            name='image',
        ),
        migrations.RemoveField(
            model_name='question',
            name='text',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='is_free',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='is_friendly',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='level',
        ),
        migrations.RemoveField(
            model_name='useranswer',
            name='created_at',
        ),
        migrations.AddField(
            model_name='question',
            name='choices',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='question',
            name='correct_answer',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='difficulty',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='question_text',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='option',
            name='text',
            field=models.TextField(),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QuizSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('score', models.IntegerField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Leaderboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('achieved_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('description', models.TextField(blank=True, null=True)),
                ('awarded_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_response', models.TextField()),
                ('is_correct', models.BooleanField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.question')),
                ('quiz_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.quizsession')),
            ],
        ),
    ]
