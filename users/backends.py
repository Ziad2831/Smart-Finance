from django.contrib.auth.backends import ModelBackend


class EmailBackend(ModelBackend):
    """Authenticate with email + password for the custom User model."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        email = kwargs.get('email') or username
        if email is None or password is None:
            return None
        return super().authenticate(
            request,
            username=email,
            password=password,
            **kwargs,
        )
