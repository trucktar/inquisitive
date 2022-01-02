import json

from django.contrib.auth import authenticate
from django.core.validators import EmailValidator
from rest_framework import exceptions, serializers

from .models import Answer, Attempt, Profile, Question, Quiz, User


def _handle_missing_fields(serializer, data):
    errors = [
        field.field_name
        for field in serializer._writable_fields
        if not data.get(field.field_name)
    ]
    if errors:
        raise serializers.ValidationError(
            detail=errors,
            code="missing_field",
        )


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def to_internal_value(self, data):
        return data

    def validate(self, data):
        _handle_missing_fields(self, data)
        errors = [
            field
            for field in ("email", "username")
            if User.objects.filter(**{field: data.get(field)}).exists()
        ]
        if errors:
            raise serializers.ValidationError(
                detail=errors,
                code="already_exists",
            )
        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password", "token"]
        read_only_fields = ["token"]
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"validators": [EmailValidator]},
        }

    def to_internal_value(self, data):
        return data

    def validate(self, data):
        _handle_missing_fields(self, data)

        email = data.get("email")
        password = data.get("password")

        user = authenticate(username=email, password=password)

        if user is None:
            raise exceptions.AuthenticationFailed(detail={"message": "Bad credentials"})

        return {"email": user.email, "token": user.token}


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source="user.email")
    username = serializers.ReadOnlyField(source="user.username")
    first_name = serializers.ReadOnlyField(source="user.first_name")
    last_name = serializers.ReadOnlyField(source="user.last_name")

    class Meta:
        model = Profile
        fields = ["email", "username", "first_name", "last_name"]


class AnswerSerializer(serializers.RelatedField):
    def to_representation(self, answer):
        return answer.value

    def to_internal_value(self, value):
        return {"value": value}


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(
        queryset=Answer.objects.all(),
        many=True,
    )

    class Meta:
        model = Question
        fields = ["id", "content", "answers"]

    def validate_answers(self, answers):
        if not answers or len(answers) != 4:
            raise serializers.ValidationError(
                detail={"answers": "A list of four possible answers is required"}
            )
        return answers


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ["id", "title", "description", "duration", "created_at", "questions"]
        read_only_fields = ["created_at"]

    def validate_questions(self, value):
        if not value:
            raise serializers.ValidationError(
                {"questions": "A list of questions is required"}
            )
        return value

    def create(self, validated_data):
        question_data = validated_data.pop("questions")
        quiz = Quiz.objects.create(**validated_data)

        for question in question_data:
            answers = question.pop("answers")
            question = Question.objects.create(quiz=quiz, **question)

            for i, answer in enumerate(answers):
                Answer.objects.create(
                    question=question,
                    value=answer["value"],
                    is_correct=not i,
                )
        return quiz


class AttemptSerializer(serializers.ModelSerializer):
    quiz_title = serializers.ReadOnlyField(source="quiz.title")
    max_score = serializers.ReadOnlyField(source="quiz.max_score")

    class Meta:
        model = Attempt
        fields = ["user_answers", "quiz_title", "score", "max_score", "percent"]
        read_only_fields = ["score", "percent"]
        extra_kwargs = {"user_answers": {"write_only": True}}

    def to_internal_value(self, data):
        data["user_answers"] = json.dumps(data["user_answers"])
        return data

    def create(self, validated_data):
        quiz = Quiz.objects.get(id=validated_data["quiz_id"])
        profile = validated_data.get("profile")

        question_ids = {q.id for q in quiz.questions}
        user_answers = json.loads(validated_data["user_answers"])

        unanswered = question_ids.difference(set(map(int, user_answers)))
        incorrect = set()
        for qn, ans in user_answers.items():
            question = Question.objects.get(id=qn)
            if not question.check_if_correct(ans):
                incorrect.add(question.id)

        score = len(question_ids - unanswered - incorrect)

        attempt = Attempt.objects.create(
            profile=profile,
            quiz=quiz,
            user_answers=validated_data["user_answers"],
            unanswered=",".join(sorted(map(str, unanswered))),
            incorrect=",".join(sorted(map(str, incorrect))),
            score=score,
        )
        return attempt
