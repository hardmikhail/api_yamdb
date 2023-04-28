from rest_framework import serializers

from reviews.models import User, Categories, Genre, Title, Review, Comments


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
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = '__all__'

    def get_rating(self, obj):
        reviews = Review.objects.filter(title=obj.id)
        if reviews.count():
            return sum([review.score for review in reviews]) / reviews.count()


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
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        score = data.get('score')
        if score < 1 or score > 10:
            raise serializers.ValidationError({'score': 'Неверное значение'})
        return (data)


class ReviewGETSerializer(serializers.ModelSerializer):
    text = serializers.CharField(required=True)
    score = serializers.IntegerField(required=True)
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )

    class Meta:
        model = Comments
        fields = '__all__'
        read_only_fields = ('pub_date',)
