from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from backend import settings
import binascii
import os
from django.utils import timezone


class CustomToken(models.Model):
    last_activity = models.DateTimeField(default=timezone.now)
    key = models.CharField("Key", max_length=40, primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='custom_auth_token',
        on_delete=models.CASCADE, verbose_name="User"
    )
    created = models.DateTimeField("Created", auto_now_add=True)

    class Meta:
        abstract = 'rest_framework.authtoken' not in settings.INSTALLED_APPS
        verbose_name = "Token"
        verbose_name_plural = "Tokens"

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(CustomToken, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key


class Organization(models.Model):
    name = models.CharField(max_length=128, unique=True)
    api_key = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return str(self.name)


class User(AbstractUser):
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)


class Object(models.Model):
    uuid = models.CharField(max_length=20, unique=True)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, blank=True, null=True)
    spinviewer = models.BooleanField(default=False)
    spinviewer_nav = models.ImageField(upload_to="uploads/objects/", blank=True, null=True, max_length=500)
    spinviewer_media = models.ImageField(upload_to="uploads/objects/", blank=True, null=True, max_length=500)
    panoviewer = models.BooleanField(default=False)
    panoviewer_nav = models.ImageField(upload_to="uploads/objects/", blank=True, null=True, max_length=500)
    panoviewer_media = models.ImageField(upload_to="uploads/objects/", blank=True, null=True, max_length=500)

    def __str__(self):
        return "Object %s" + self.uuid


class Annnotation(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="uploads/annnotations/", blank=True, null=True, max_length=500)
    description = models.TextField(max_length=500)
    annotation = models.ForeignKey(Object, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return str(self.title)


class AnnnotationPos(models.Model):
    annotation = models.ForeignKey(Annnotation, on_delete=models.CASCADE, null=False)
    position_x = models.PositiveIntegerField(validators=[MaxValueValidator(100), MinValueValidator(1)])
    position_y = models.PositiveIntegerField(validators=[MaxValueValidator(100), MinValueValidator(1)])

    class Meta:
        verbose_name = "AnnotationPos"
        verbose_name_plural = "AnnotationPos"

    def __str__(self):
        return str('Annotation Pos ' + str(self.id) + ' X:' + str(self.position_x) + ' Y:' + str(self.position_y))
