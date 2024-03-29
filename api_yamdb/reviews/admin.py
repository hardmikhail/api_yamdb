from django.contrib import admin

from .models import (Title,
                     Categories,
                     Genre,
                     GenreTitle,
                     Comments,
                     Review
                     )


admin.site.register(Title)
admin.site.register(Categories)
admin.site.register(Genre)
admin.site.register(GenreTitle)
admin.site.register(Review)
admin.site.register(Comments)
