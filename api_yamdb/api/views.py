from rest_framework import mixins, filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import (
    CategoriesSerializer,
    GenreSerializer,
    TitleGETSerializer,
    TitleSerializer,
)
from review.models import Categories, Genre, Title
from .filters import TitleFilter

class CategoriesViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
    ):
    """Вьюсет для создания обьектов класса Category."""

    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    # permission_classes = (ReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
    ):
    """Вьюсет для создания обьектов класса Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # permission_classes = (ReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для создания обьектов класса Title."""

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    # permission_classes = (ReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    
    def get_serializer_class(self):
        """Определяет какой сериализатор будет использоваться
        для разных типов запроса."""
        if self.request.method == 'GET':
            return TitleGETSerializer
        return TitleSerializer
