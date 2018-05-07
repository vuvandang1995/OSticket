from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from user.models import active
class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(active(user))
        )
account_activation_token = TokenGenerator()