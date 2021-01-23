from django.conf.urls import url
from django.urls import path, include
import main.api
from . import views

urlpatterns = [
    path(r'api', include('rest_framework.urls')),
    url(r'api/object/(?P<uuid>[-\w]+)/?', main.api.ObjectDetail.as_view()),
    url(r'api/object/?', main.api.ObjectListCreate.as_view()),
    url(r'api/pano-annotation/(?P<id>[-\w]+)/?', main.api.PanoAnnotationDetail.as_view()),
    url(r'api/pano-annotation/?', main.api.PanoAnnotationListCreate.as_view()),
    url(r'api/annotation/(?P<id>[-\w]+)/?', main.api.AnnotationDetail.as_view()),
    url(r'api/annotation/?', main.api.AnnotationListCreate.as_view()),
    url(r'api/user/?', main.api.UserSelfUpdateDetail.as_view()),
    url(r'sample', views.sample, name="sample"),
    url(r'view/(?P<key>[-\w]+)/(?P<uuid>[-\w]+)', views.view_object, name="view_object"),
    url(r'spinviewer/(?P<key>[-\w]+)/(?P<uuid>[-\w]+)', views.view_spinviewer, name="view_spinviewer"),
    url(r'panoviewer/(?P<key>[-\w]+)/(?P<uuid>[-\w]+)', views.view_panoviewer, name="view_panoviewer")
]
