# Generated by Django 4.2.17 on 2025-01-14 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0011_alter_question_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='quiz_type',
            field=models.CharField(choices=[('web_programming', 'Web Programming'), ('database', 'Database'), ('python', 'Python'), ('javascript', 'JavaScript'), ('c_programming', 'C Programming'), ('networking', 'Networking')], default='web_programming', max_length=50),
        ),
    ]