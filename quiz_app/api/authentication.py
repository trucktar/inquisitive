import jwt
from django.conf import settings
from rest_framework import authentication, exceptions

from .models import User


class JWTAuthentication(authentication.TokenAuthentication):
    """
    JWT based authentication.

    Clients should authenticated by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:

        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
    """
    def authenticate_credentials(self, token):
        """
        Attempts to find and return a user using the given token.
        """
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=['HS256'],
            )
        except:
            msg = 'Invalid or expired token.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            msg = 'Token contained no recognizable user identification.'
            raise exceptions.AuthenticationFailed(msg)

        return (user, token)
