from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Profile
from ..serializers import ProfileSerializer


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    http_method_names = ['get', 'put']

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = self.serializer_class(profile)

        return Response(serializer.data, status=status.HTTP_302_FOUND)

    def put(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = self.serializer_class(profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(
            {
                'message': 'Update failed!',
                'errors': {
                    **serializer.errors,
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
