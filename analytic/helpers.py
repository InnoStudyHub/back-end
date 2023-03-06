import datetime

from analytic.models import UserAnalyticModel, EventsModel
from user.models import StudyhubUserAnalyticModel


def get_user_analytic(user_id):
    is_anonymous = False
    if user_id is None:
        is_anonymous = True

    user_analytic = None
    if not StudyhubUserAnalyticModel.objects.filter(studyhub_user_id=user_id):
        user_analytic = UserAnalyticModel.objects.create(is_anonymous=is_anonymous)
        if not is_anonymous:
            StudyhubUserAnalyticModel.objects.create(user_analytic_id=user_analytic.user_analytic_id,
                                                     studyhub_user_id=user_id)
    else:
        user_analytic_id = StudyhubUserAnalyticModel.objects.get(studyhub_user_id=user_id).user_analytic_id
        user_analytic = UserAnalyticModel.objects.get(user_analytic_id=user_analytic_id)

    return user_analytic


def add_event(user, event_category):
    user_id = None
    if user.is_authenticated:
        user_id = user.id

    user_analytic = get_user_analytic(user_id)

    now = datetime.datetime.now()

    EventsModel.objects.create(event_category=event_category, user_analytic=user_analytic,
                               event_time=now)
