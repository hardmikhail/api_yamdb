from django.contrib import admin

from .models import Categories, Genre, Title, User, Review, Comments, GenreTitle

admin.site.register(GenreTitle)
admin.site.register(Categories)
admin.site.register(Comments)
admin.site.register(Review)
admin.site.register(User)
admin.site.register(Title)
admin.site.register(Genre)