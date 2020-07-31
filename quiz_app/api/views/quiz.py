from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Attempt, Quiz
from ..serializers import AttemptSerializer, QuizSerializer


class QuizListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuizSerializer
    http_method_names = ['get', 'post']

    def get(self, request):
        quizzes = Quiz.objects.all()
        serializer = self.serializer_class(quizzes, many=True)

        return Response(serializer.data, status=status.HTTP_302_FOUND)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save(profile=request.user.profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(
            {
                'message': 'Quiz creation failed',
                'errors': {
                    **serializer.errors,
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class AttemptView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AttemptSerializer
    http_method_names = ['post']

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            quiz_id = serializer.validated_data['quiz_id']
            if Attempt.objects.filter(
                    quiz_id=quiz_id,
                    profile=request.user.profile,
            ).exists():
                return Response(
                    {
                        'status': 'error',
                        'message': 'Quiz has been attempted before',
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer.save(profile=request.user.profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(
            {
                'status': 'error',
                'message': 'Attempt creation failed',
                'errors': {
                    **serializer.errors,
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
