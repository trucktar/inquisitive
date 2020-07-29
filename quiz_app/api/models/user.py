from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email and password.
        """
        if username is None:
            raise ValueError('The given username must be set')
        if email is None:
            raise ValueError('The given email must be set')
        if password is None:
            raise ValueError('The given password must be set')

        email = email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        """Returns a string representation of `User` instance."""
        return self.email

    @property
    def token(self):
        """Gets the generated JWT for this user's id."""
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode(
            {
                'id': self.pk,
                'exp': int(dt.strftime('%s'))
            },
            settings.SECRET_KEY,
            algorithm='HS256',
        )

        return token.decode()
