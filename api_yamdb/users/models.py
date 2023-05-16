from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import validate_email
from django.db import models

USER_ROLE = 'user'
ADMIN_ROLE = 'admin'
MODERATOR_ROLE = 'moderator'

ROLES = (
    (USER_ROLE, USER_ROLE.title()),
    (ADMIN_ROLE, ADMIN_ROLE.title()),
    (MODERATOR_ROLE, MODERATOR_ROLE.title()),
)


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text=('Required. 150 characters or fewer. Letters, '
                   'digits and @/./+/-/_ only.'),
        validators=[UnicodeUsernameValidator()],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    email = models.CharField(
        max_length=254,
        unique=True,
        help_text='Required. 254 characters or fewer.',
        validators=[validate_email],
        error_messages={
            'unique': "A user with that email already exists.",
        },
    )

    bio = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=32, choices=ROLES, default=USER_ROLE)

    class Meta:
        ordering = ['-id']

    @property
    def is_admin(self):
        return self.role == ADMIN_ROLE

    @property
    def is_moderator(self):
        return self.role == MODERATOR_ROLE
