from django.urls import path

from .views import RegistrationAPIView, UserAPIView, \
    LogoutAPIView, UserIULoginView, MyTokenRefreshView
from .views import MyObtainTokenPairView

urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='user_login'),
    path('logout/', LogoutAPIView.as_view(), name='user_logout'),
    path('login/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegistrationAPIView.as_view(), name='user_register'),
    path('info/',  UserAPIView.as_view(), name='user_info'),
    path('login/iu/', UserIULoginView.as_view({"post": "auth_iu_with_code"}), name='user_iu_login'),
]
