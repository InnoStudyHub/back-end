from django.db import models


class UserAnalyticModel(models.Model):
    user_analytic_id = models.AutoField(primary_key=True)
    is_anonymous = models.BooleanField(default=True)
    app_launches = models.IntegerField(default=0)

    class Meta:
        db_table = 'analytic_user'


class AppLaunchModel(models.Model):
    app_launch_id = models.AutoField(primary_key=True)
    user_analytic = models.ForeignKey(UserAnalyticModel, on_delete=models.CASCADE)
    platform = models.CharField(max_length=256)
    ip_address = models.CharField(max_length=256, blank=True, null=True)
    country = models.CharField(max_length=256, blank=True, null=True)
    region_name = models.CharField(max_length=256, blank=True, null=True)
    city = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        db_table = 'app_launch'


class EventsCategoryModel(models.Model):
    event_category_id = models.AutoField(primary_key=True)
    event_category_name = models.CharField(max_length=256)

    class Meta:
        db_table = 'event_category'


class EventsModel(models.Model):
    event_id = models.AutoField(primary_key=True)
    user_analytic = models.ForeignKey(UserAnalyticModel, on_delete=models.CASCADE)
    event_category = models.ForeignKey(EventsCategoryModel, on_delete=models.CASCADE)
    event_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'events'



