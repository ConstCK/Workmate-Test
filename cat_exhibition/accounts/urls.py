from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import RegistrationAPIView, LogInAPIView, LogOutAPIView

urlpatterns = [
    path('signup/', RegistrationAPIView.as_view(), name='signup'),
    path('login/', LogInAPIView.as_view(), name='login'),
    path('logout/', LogOutAPIView.as_view(), name='logout'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ]
