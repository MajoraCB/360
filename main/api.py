from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.authentication import SessionAuthentication
from .auth import InactivityTokenAuthentication


class UserSelfUpdateDetail(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (InactivityTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        target = User.objects.filter(id=self.request.user.id)

        if target.count() != 1:
            raise ValueError("Error getting user " + (str(self.request.user)))
        return target


class ObjectDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'uuid'
    serializer_class = ObjectSerializer
    authentication_classes = (InactivityTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        user = self.request.user
        objects = Object.objects.filter(organization=user.organization)
        return objects


class ObjectListCreate(generics.ListCreateAPIView):
    serializer_class = ObjectSerializer
    authentication_classes = (InactivityTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        user = self.request.user
        objects = Object.objects.filter(organization=user.organization)
        return objects
