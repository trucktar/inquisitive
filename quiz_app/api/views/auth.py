from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import LoginSerializer, SignupSerializer


def _handler_422(serializer):
    """
    Return a response with status code 422 and application/json content type.
    """
    return Response(
        {
            "message": "Validation failed",
            "errors": [
                {"field": err, "code": err.code}
                for err in serializer.errors.pop("errors")
            ],
        },
        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


class SignupAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SignupSerializer
    http_method_names = ["post"]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Registration successful"}, status=status.HTTP_201_CREATED
            )
        return _handler_422(serializer)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    http_method_names = ["post"]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response(
                {
                    "message": "Login successful",
                    "token": serializer.validated_data["token"],
                },
                status=status.HTTP_200_OK,
            )
        return _handler_422(serializer)
