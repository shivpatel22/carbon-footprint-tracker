from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UserProfile, ActivityLog, UploadRecord

admin.site.register(UserProfile)
admin.site.register(ActivityLog)
admin.site.register(UploadRecord)
