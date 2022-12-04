from django.urls import path
from deck.views import CoursesAPIView

urlpatterns = [
    path('add/', CoursesAPIView.as_view(), name='course_add'),
]
