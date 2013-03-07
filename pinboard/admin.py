from django.contrib import admin
from pinboard.models import PinboardPost, Category, ImageSize

admin.site.register(PinboardPost)
admin.site.register(Category)
admin.site.register(ImageSize)
