
from django.db import models
from django.contrib.auth.models import User


class QuizAttempt(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="quiz_attempts",
    )
    student_name = models.CharField(max_length=100, default="Student")
    score = models.PositiveIntegerField()
    total_questions = models.PositiveIntegerField()
    percentage = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} - {self.percentage}%"


class TopicScore(models.Model):
    attempt = models.ForeignKey(
        QuizAttempt,
        on_delete=models.CASCADE,
        related_name="topic_scores",
    )
    topic_name = models.CharField(max_length=100)
    correct_answers = models.PositiveIntegerField()
    total_questions = models.PositiveIntegerField()
    percentage = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.topic_name} - {self.percentage}%"
