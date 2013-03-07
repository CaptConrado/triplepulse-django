from django.db import models
from cms.models import pagemodel

class ImageSize(models.Model):
    width = models.IntegerField()
    height = models.IntegerField()
    name = models.CharField(max_length=128)
    def __unicode__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=128)
    verbose_name = models.CharField(max_length=128)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Categories"

class PinboardPost(models.Model):
    page = models.ForeignKey(pagemodel.Page)
    image = models.ImageField(upload_to="pinboard_images")
    image_size = models.ForeignKey(ImageSize)
    category = models.ForeignKey(Category)
    def __unicode__(self):
        return unicode(self.page)