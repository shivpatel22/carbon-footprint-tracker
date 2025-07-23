from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    join_date = models.DateTimeField(auto_now_add=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    # ✅ Add this line
    monthly_co2_goal = models.FloatField(default=20.0)  # Default 20kg, or choose your default

    def __str__(self):
        return self.user.username


class ActivityLog(models.Model):
    ACTIVITY_CHOICES = [
        ('travel', 'Travel'),
        ('electricity', 'Electricity'),
        ('food', 'Food Consumption'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_CHOICES)
    description = models.CharField(max_length=255)
    input_value = models.FloatField(help_text="Distance in km, kWh used, or meals eaten")
    co2_emitted = models.FloatField(editable=False, null=True) # auto-computed
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} - {self.co2_emitted:.2f} kg"



class UploadRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    upload = models.FileField(upload_to='uploads/')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"


# # CO₂ activity log
# class Activity(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     activity_name = models.CharField(max_length=100)
#     co2_emission = models.FloatField(help_text="CO₂ in kg")
#     date = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.activity_name} - {self.co2_emission} kg"
#


# # Optional: if you haven't already extended user
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     monthly_co2_goal = models.FloatField(default=0.0)  # in kg
#
#     def __str__(self):
#         return f"{self.user.username}'s Profile"