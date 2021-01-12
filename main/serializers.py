from rest_framework import serializers
from .models import Object
from .utils import *


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
    uuid = serializers.CharField()
    spinviewer = serializers.BooleanField()
    panoviewer = serializers.BooleanField()
    spinviewer_nav = serializers.ImageField(required=False, allow_null=True)
    spinviewer_media = serializers.ImageField(required=False, allow_null=True)
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
                o.spinviewer_nav = spinviewer_photos[0]
                o.spinviewer_media = generate_sprite_image(spinviewer_photos)
            else:
                raise serializers.ValidationError('{"error": "Missing required spinviewer images" }')

        if validated_data['panoviewer']:
            panoviewer_photo = request.FILES.getlist('panoviewer_photo')
            if len(panoviewer_photo) > 0:
                # o.panoviewer_media = panoviewer_photo[0]
                o.panoviewer_nav = panoviewer_photo[0]
            else:
                raise serializers.ValidationError('{"error": "Missing required panoviewer image" }')

        o.save()

        return o

    class Meta:
        depth = 1
