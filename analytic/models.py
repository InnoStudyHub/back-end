from django.db import models

from user.models import User


class UserAnalytic(models.Model):
    user_analytic_id = models.AutoField(primary_key=True)
    studyhub_user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_analytic'


class UserProperties(models.Model):
    user_properties_id = models.AutoField(primary_key=True)
    user_analytic_id = models.ForeignKey(UserAnalytic, on_delete=models.CASCADE)
    launch_count = models.IntegerField(default=0)
    platform = models.CharField(max_length=256)
    year = models.IntegerField(blank=True, null=True)
    country = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        db_table = 'user_properties'


class AppEvents(models.Model):
    app_event_id = models.AutoField(primary_key=True)
    user_analytic_id = models.ForeignKey(UserAnalytic, on_delete=models.CASCADE)
    session_start_time = models.DateTimeField(blank=True, null=True)
    session_end_time = models.DateTimeField(blank=True, null=True)
    app_background_time = models.DateTimeField(blank=True, null=True)
    app_foreground_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'app_event'



