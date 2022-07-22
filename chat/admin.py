from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(GroupChat)
admin.site.register(Member)
admin.site.register(Message)
admin.site.register(VideoThread)