from django.contrib import admin

from User.models import Profile
from .models import PrivateModel, Private_SubModel

admin.site.register(PrivateModel)
admin.site.register(Private_SubModel)
admin.site.register(Profile)
