from django.contrib import admin
from .models import BlogModel, CommentsModel

admin.site.register(BlogModel)
admin.site.register(CommentsModel)

