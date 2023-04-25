from rest_framework import serializers

from reviews.models import User, Categories, Genre, Title, Review


class UserSignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.SlugField(required=True, max_length=150)

    class Meta:
        fields = ('email', 'username')
        model = User


class ObtainTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        model = User


class UsersMeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio'
        )
        model = User


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Categories."""

    class Meta:
        model = Categories
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        model = Genre
        exclude = ('id',)


class TitleGETSerializer(serializers.ModelSerializer):
    """Сериализатор объектов класса Title при GET запросах."""
    genre = GenreSerializer(many=True, read_only=True)
    category = CategoriesSerializer(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор объектов класса Title при небезопасных запросах."""
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    text = serializers.CharField(required=True, max_length=1000)
    score = serializers.IntegerField(required=True)
    # author = serializers.RelatedField(queryset=Reviews.objects.all())

    class Meta:
        # fields = ('id', 'text', 'author', 'score', 'pub_date')
        fields = ('id', 'text', 'score', 'pub_date')
        read_only_fields = ('author',)
        model = Review