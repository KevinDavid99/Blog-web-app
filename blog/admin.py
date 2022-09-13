from django.contrib import admin
from .models import Post, CreateImages, LikePost
# Register your models here.

admin.site.register(Post)
admin.site.register(CreateImages)
admin.site.register(LikePost)