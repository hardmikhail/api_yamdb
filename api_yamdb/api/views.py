from rest_framework import mixins, filters, viewsets

from .serializers import (
    CategoriesSerializer,
    GenreSerializer,
    TitleGETSerializer,
    TitleSerializer,
)
from review.models import Categories, Genre, Title
from .filters import TitleFilter
from .permissions import IsAdminOrReadOnly

class CategoriesViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
    ):
    """Вьюсет для создания обьектов класса Category."""

    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
    ):
    """Вьюсет для создания обьектов класса Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для создания обьектов класса Title."""

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleFilter
    
    def get_serializer_class(self):
        """Определяет какой сериализатор будет использоваться
        для разных типов запроса."""
        if self.action in ('list', 'retrieve'):
            return TitleGETSerializer
        return TitleSerializer
