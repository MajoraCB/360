from django.shortcuts import render
from .models import *
from django.http import Http404
from django.shortcuts import redirect
from .serializers import *


def sample(request):
    return render(request, 'main/sample.html')


def view_object(request, key, uuid):
    try:
        object = Object.objects.get(organization__api_key=key, uuid=uuid)
    except Object.DoesNotExist:
        raise Http404("Object does not exist")

    if object.spinviewer:
        return redirect('view_spinviewer', key=key, uuid=uuid)

    if object.panoviewer:
        return redirect('view_panoviewer', key=key, uuid=uuid)


def view_panoviewer(request, key, uuid):
    try:
        object = Object.objects.get(organization__api_key=key, uuid=uuid)
    except Object.DoesNotExist:
        raise Http404("Object does not exist")

    try:
        annotations = PanoAnnotation.objects.filter(object=object)
    except PanoAnnotation.DoesNotExist:
        annotations = []

    context = {
        'object': object,
        'annotations': json.dumps(PanoAnnotationSeriralizer(annotations, many=True).data)
    }

    return render(request, 'main/view_panoviewer.html', context)


def view_spinviewer(request, key, uuid):
    try:
        object = Object.objects.get(organization__api_key=key, uuid=uuid)
    except Object.DoesNotExist:
        raise Http404("Object does not exist")

    try:
        annotations = Annotation.objects.filter(object=object)
    except PanoAnnotation.DoesNotExist:
        annotations = []

    context = {
        'object': object,
        'annotations':  json.dumps(AnnotationSeriralizer(annotations, many=True).data)
    }

    return render(request, 'main/view_spinviewer.html', context)
