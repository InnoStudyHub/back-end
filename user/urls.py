from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import RegistrationAPIView, UserAPIView, LogoutAPIView, UserIULoginView
from .views import MyObtainTokenPairView

urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='user_login'),
    path('logout/', LogoutAPIView.as_view(), name='user_logout'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegistrationAPIView.as_view(), name='user_register'),
    path('info/',  UserAPIView.as_view(), name='user_info'),
    path('login/iu/', UserIULoginView.as_view({"post": "auth_iu_with_code"}), name='user_iu_login'),
]