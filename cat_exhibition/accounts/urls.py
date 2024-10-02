from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import RegistrationAPIView, LogInAPIView, LogOutAPIView

urlpatterns = [
    path('signup/', RegistrationAPIView.as_view(), name='signup'),
    path('login/', LogInAPIView.as_view(), name='login'),
    path('logout/', LogOutAPIView.as_view(), name='logout'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ]
