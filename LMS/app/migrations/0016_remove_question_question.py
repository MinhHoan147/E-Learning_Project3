# Generated by Django 4.1.5 on 2023-02-01 09:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_remove_quizzes_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='question',
        ),
    ]
