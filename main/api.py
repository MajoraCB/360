from rest_framework import generics
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
        objects = Object.objects.filter(organization=user.organization).order_by(
            'uuid')
        return objects


class AnnotationDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = AnnotationSeriralizer
    authentication_classes = (InactivityTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        annotations = Annotation.objects.filter(object__organization=self.request.user.organization).order_by(
            'title')
        return annotations


class AnnotationListCreate(generics.ListCreateAPIView):
    serializer_class = AnnotationSeriralizer
    authentication_classes = (InactivityTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        if self.request.GET.get('uuid'):
            annotations = Annotation.objects.filter(object__uuid=self.request.GET.get('uuid')).order_by(
                'title')
            return annotations
        else:
            annotations = Annotation.objects.filter(object__organization=self.request.user.organization).order_by(
                'title')
            return annotations


class PanoAnnotationDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = PanoAnnotationSeriralizer
    authentication_classes = (InactivityTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        annotations = PanoAnnotation.objects.filter(object__organization=self.request.user.organization).order_by(
            'title')
        return annotations


class PanoAnnotationListCreate(generics.ListCreateAPIView):
    serializer_class = PanoAnnotationSeriralizer
    authentication_classes = (InactivityTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        if self.request.GET.get('uuid'):
            annotations = PanoAnnotation.objects.filter(object__uuid=self.request.GET.get('uuid')).order_by(
                'title')
            return annotations
        else:
            annotations = PanoAnnotation.objects.filter(object__organization=self.request.user.organization).order_by(
                'title')
            return annotations
