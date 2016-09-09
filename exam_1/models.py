from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class Quiz(models.Model):
    quiz_title = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    expired_date = models.DateTimeField(
        null=True, blank=True)

    def __str__(self):
        return self.quiz_title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)
    #~ answer = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    def __str__(self):
        return self.choice_text


class UserSession(models.Model):
    user = models.ForeignKey(User)
    quiz = models.ForeignKey(Quiz)
    question = models.ForeignKey(Question)
    user_answer = models.ForeignKey(Choice, default='')
    user_score = models.IntegerField()
    answered_date = models.DateTimeField(default=timezone.now)

    def is_passed(self):  # tignan kung pasado
        if self.user_score >= 75:
            return 'Passed'
        else:
            return 'Failed'

    def correct_answer(self):
        return self.question.answer

    def is_correct(self):
        correct_answer = str(self.correct_answer()).strip().lower()
        user_answer = str(self.user_answer).strip().lower()
        
        if correct_answer == user_answer:
            return True
        else:
            return False
