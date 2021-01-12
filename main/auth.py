from datetime import datetime, timedelta

import pytz
from django.conf import settings
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication
from main.models import CustomToken


class InactivityTokenAuthentication(TokenAuthentication):
    model = CustomToken

    def authenticate_credentials(self, key):
        key = key.strip()
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            print("invalid token!!")
            raise exceptions.NotAuthenticated('Invalid token.')

        if not token.user.is_active:
            raise exceptions.NotAuthenticated('User inactive or deleted.')

        utc_now = datetime.utcnow()
        utc_now = utc_now.replace(tzinfo=pytz.utc)

        if token.last_activity < utc_now - timedelta(minutes=settings.TOKEN_TIMEOUT):
            token.delete()
            print("Token has expired!!")
            raise exceptions.NotAuthenticated('Token has expired')

        token.last_activity = utc_now
        token.save()

        return token.user, token
