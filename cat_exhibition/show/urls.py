from django.urls import path, include
from rest_framework import routers

from .views import CatsViewSet, BreedViewSet, VoteAPIView
router = routers.DefaultRouter()
router.register('cats', CatsViewSet, basename='cats')
router.register('breeds', BreedViewSet, basename='breeds')


urlpatterns = [
    path('', include(router.urls)),
    path('voting/<int:cat_id>/', VoteAPIView.as_view(), name='vote'),
]
