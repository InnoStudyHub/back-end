from django.db import models

class AppLaunchModel(models.Model):
    app_launch_id = models.AutoField(primary_key=True)
    platform = models.CharField(max_length=256)
    ip_address = models.CharField(max_length=256, blank=True, null=True)
    is_logged = models.BooleanField(default=False)
    country = models.CharField(max_length=256, blank=True, null=True)
    region_name = models.CharField(max_length=256, blank=True, null=True)
    city = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        db_table = 'app_launch'


class AppEventsModel(models.Model):
    app_event_id = models.AutoField(primary_key=True)
    user_analytic_id = models.ForeignKey(AppLaunchModel, on_delete=models.CASCADE)
    session_start_time = models.DateTimeField(blank=True, null=True)
    session_end_time = models.DateTimeField(blank=True, null=True)
    app_background_time = models.DateTimeField(blank=True, null=True)
    app_foreground_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'app_event'



