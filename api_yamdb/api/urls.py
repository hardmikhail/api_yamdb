from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CategoriesViewSet, GenreViewSet, TitleViewSet
)

router = DefaultRouter()
router.register('categories', CategoriesViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('', include(router.urls))
]
