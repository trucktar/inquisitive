import json

from django.core.validators import validate_comma_separated_integer_list
from django.db import models

from .profile import Profile


class Quiz(models.Model):
    title = models.CharField(max_length=60)
    description = models.TextField(help_text="A description of the quiz")
    duration = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        ordering = ["created_at"]
        verbose_name_plural = "quizzes"

    @property
    def questions(self):
        return self.question_set.filter(quiz=self)

    @property
    def max_score(self):
        return self.questions.count()


class Question(models.Model):
    content = models.CharField(
        max_length=1000,
        help_text="The question text to be displayed",
    )

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    @property
    def answers(self):
        """Get all answers for a question."""
        return self.answer_set.filter(question=self)

    def check_if_correct(self, value):
        answer = Answer.objects.get(question=self, value=value)
        return answer.is_correct


class Answer(models.Model):
    value = models.CharField(
        max_length=1000,
        help_text="The answer text to be displayed",
    )
    is_correct = models.BooleanField(default=False)

    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.value


class Attempt(models.Model):
    user_answers = models.TextField(
        default="{}",
        help_text="JSON object that maps question ids to user answers",
    )
    unanswered = models.CharField(
        max_length=1024,
        validators=[validate_comma_separated_integer_list],
        help_text="A list of integer ids of all unanswered questions",
    )
    incorrect = models.CharField(
        max_length=1024,
        validators=[validate_comma_separated_integer_list],
        help_text="A list of integer ids of all incorrectly answered questions",
    )
    score = models.IntegerField()

    quiz = models.OneToOneField(Quiz, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    @property
    def percent(self):
        return (int(self.score) / self.quiz.max_score) * 100
