from rest_framework import serializers
from .models import *
from .utils import *
import json


class OrganizationSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField()
    key = serializers.CharField(read_only=True)


class UserSerializer(serializers.Serializer):
    last_login = serializers.DateTimeField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True, required=False)
    username = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    organization = OrganizationSerializer(required=False, allow_null=True)


class ObjectSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    uuid = serializers.CharField()
    spinviewer = serializers.BooleanField()
    panoviewer = serializers.BooleanField()
    spinviewer_nav = serializers.ImageField(required=False, allow_null=True)
    spinviewer_media = serializers.ImageField(required=False, allow_null=True)
    spinviewer_row_count = serializers.IntegerField(required=False)
    spinviewer_col_count = serializers.IntegerField(required=False)
    panoviewer_nav = serializers.ImageField(required=False, allow_null=True)
    panoviewer_media = serializers.ImageField(required=False, allow_null=True)
    organization = OrganizationSerializer(required=False)

    def create(self, validated_data):
        request = self.context['request']

        o = Object(**validated_data)

        if request.user.organization:
            o.organization = request.user.organization
        else:
            raise serializers.ValidationError('{"error": "User has no organization" }')

        if validated_data['spinviewer']:
            spinviewer_photos = request.FILES.getlist('spinviewer_photos')
            if spinviewer_photos and len(spinviewer_photos) > 0:
                o.spinviewer_nav = generate_sprite_nav_image(spinviewer_photos[0])
                sprite_data = generate_sprite_image(spinviewer_photos)
                o.spinviewer_media = sprite_data[0]
                o.spinviewer_col_count = sprite_data[1]
                o.spinviewer_row_count = sprite_data[2]
            else:
                raise serializers.ValidationError('{"error": "Missing required spinviewer images" }')

        if validated_data['panoviewer']:
            panoviewer_photo = request.FILES.getlist('panoviewer_photo')
            if len(panoviewer_photo) > 0:
                o.panoviewer_media = panoviewer_photo[0]
                o.panoviewer_nav = generate_panoviewer_nav_image(panoviewer_photo[0])
            else:
                raise serializers.ValidationError('{"error": "Missing required panoviewer image" }')

        o.save()

        return o

    class Meta:
        depth = 1


class AnnotationPosSeriralizer(serializers.Serializer):
    frame_index = serializers.IntegerField(default=0)
    position_x = serializers.FloatField(default=0)
    position_y = serializers.FloatField(default=0)


class AnnotationSeriralizer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=100, required=True)
    photo = serializers.ImageField(required=True)
    description = serializers.CharField(max_length=500, required=True)
    object = ObjectSerializer(required=False)
    annotationPoses = AnnotationPosSeriralizer(source='annotationpos_set', many=True, required=False, allow_null=True)

    def create(self, validated_data):
        request = self.context['request']

        if request.POST.get('object'):
            object = Object.objects.get(pk=request.POST.get('object'))
        else:
            raise serializers.ValidationError('{"error": "Missing required object" }')

        annotation = Annotation(**validated_data)
        annotation.object = object
        annotation.save()

        if request.POST.get('annotationPoses'):
            annotationPoses = json.loads(request.POST.get('annotationPoses'))
            for annotationPosData in annotationPoses:
                annotationPos = AnnotationPos(**annotationPosData)
                annotationPos.annotation = annotation
                annotationPos.save()

        return annotation

    def update(self, instance, validated_data):
        instance.title = validated_data['title']
        instance.description = validated_data['description']

        if 'photo' in validated_data:
            instance.photo = validated_data['photo']

        instance.save()

        request = self.context['request']

        if request.POST.get('annotationPoses'):
            instance.annotationpos_set.all().delete()
            annotationPoses = json.loads(request.POST.get('annotationPoses'))
            for annotationPosData in annotationPoses:
                annotationPos = AnnotationPos(**annotationPosData)
                annotationPos.annotation = instance
                annotationPos.save()

        return instance



class PanoAnnotationSeriralizer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=100, required=True)
    photo = serializers.ImageField(required=True)
    description = serializers.CharField(max_length=500, required=True)
    object = ObjectSerializer(required=False)
    yaw = serializers.FloatField(default=0)
    pitch = serializers.FloatField(default=0)

    def create(self, validated_data):
        request = self.context['request']

        if request.POST.get('object'):
            object = Object.objects.get(pk=request.POST.get('object'))
        else:
            raise serializers.ValidationError('{"error": "Missing required object" }')

        annotation = PanoAnnotation(**validated_data)
        annotation.object = object
        annotation.save()

        return annotation

    def update(self, instance, validated_data):
        instance.title = validated_data['title']
        instance.description = validated_data['description']
        instance.yaw = validated_data['yaw']
        instance.pitch = validated_data['pitch']

        if 'photo' in validated_data:
            instance.photo = validated_data['photo']

        instance.save()

        return instance