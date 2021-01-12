from django.conf.urls import url
from django.urls import path, include
import main.api

urlpatterns = [
    path('', include('rest_framework.urls')),
    url(r'object/(?P<uuid>[-\w]+)/?', main.api.ObjectDetail.as_view()),
    url(r'object/?', main.api.ObjectListCreate.as_view()),
    url(r'user/?', main.api.UserSelfUpdateDetail.as_view()),
]
