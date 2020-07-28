from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import LoginSerializer, SignupSerializer


class SignupAPIView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = SignupSerializer
    http_method_names = ['post']

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    'message': 'Registration failed!',
                    'errors': {
                        **serializer.errors,
                    },
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = LoginSerializer
    http_method_names = ['post']

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            # Authenticating with invalid credentials returns 401 Unauthorized
            return Response(
                {
                    'message': 'Bad credentials',
                    'errors': {
                        **serializer.errors,
                    },
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return Response(serializer.data, status=status.HTTP_200_OK)
