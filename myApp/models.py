import os
from datetime import date
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import AbstractUser
from django.db import models
from ckeditor.fields import RichTextField


# User = get_user_model()
class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pictures/', default="/default_images/patient_pic.png")
    email = models.CharField(max_length=255, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    age = models.PositiveSmallIntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.email:
            username = str(self.email).split("@")[0]
            self.username = username

        if self.birth_date:
            self.age = relativedelta(date.today(), self.birth_date).years
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        # Delete the associated image when the instance is deleted
        if self.profile_picture and 'default_images' not in self.profile_picture.name:
            if os.path.isfile(self.profile_picture.path):
                os.remove(self.profile_picture.path)

    def __str__(self):
        return self.username


class BlogCategoryDb(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250, default="", blank=True, null=True)
    status = models.BooleanField(default=True)
    description = models.TextField(default="", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


# Blog db
class BlogDb(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(BlogCategoryDb, on_delete=models.CASCADE, related_name='blog')
    tags = models.ManyToManyField(Tag, related_name='blogs')
    title = models.CharField(max_length=255, default="", blank=True, null=True)
    type = models.CharField(max_length=255, default="", blank=True, null=True)
    description = RichTextField(default="", blank=True, null=True)
    meta_keyword = models.CharField(max_length=255, default="", blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='article_images', blank=True, null=True)
    status = models.BooleanField(default=True)
    published_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    likes = models.CharField(max_length=255, default="", blank=True, null=True)
    views = models.CharField(max_length=255, default="", blank=True, null=True)
    comments = models.CharField(max_length=255, default="", blank=True, null=True)

    def __str__(self):
        return str(self.id)


class BlogCommentsDb(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(BlogDb, on_delete=models.CASCADE)
    comment = models.TextField(default='', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
