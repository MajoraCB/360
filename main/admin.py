from django.contrib import admin
from .models import *


class ObjectAdmin(admin.ModelAdmin):
    search_fields = ('uuid',)


class UserAdmin(admin.ModelAdmin):
    exclude = ("passowrd",)
    readonly_fields = ("password",)


admin.site.register(User, UserAdmin)
admin.site.register(Object, ObjectAdmin)
admin.site.register(Organization)
