import os.path

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from markdownx.utils import markdown
from markdownx.models import MarkdownxField


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/review/tag/{self.slug}'

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/review/category/{self.slug}'

    class Meta:
        verbose_name_plural = 'Categories'


class Review(models.Model):
    title = models.CharField(max_length=30)
    content = MarkdownxField()

    attached_file = models.FileField(upload_to='review/files/%Y/%m/%d/', blank=True)

    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'[{self.pk}]  {self.title} :: {self.author}'

    def get_absolute_url(self):
        return f'/review/{self.pk}/'

    def get_file_name(self):
        return os.path.basename(self.attached_file.name)

    def get_content_markdown(self):
        return markdown(self.content)

class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}::{self.content}'

    def get_absolute_url(self):
        return f'{self.review.get_absolute_url()}#comment-{self.pk}'