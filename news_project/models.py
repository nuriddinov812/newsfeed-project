from django.db import models
from django.utils import timezone

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='PB') 



class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class News(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'draft'
        PUBLISHED = 'PB', 'published'
    
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True)
    body = models.TextField()
    image = models.FileField(upload_to='images/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    publish_time = models.DateTimeField(default=timezone.now)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT
    )
    views_count = models.PositiveIntegerField(default=0)
    objects = models.Manager()
    published = PublishedManager()
    
    class Meta:
        ordering = ['-publish_time']
    
    def __str__(self):
        return self.title


class Contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    massage=models.TextField()
    
    def __str__(self):
        return self.email
    
    
class Comments(models.Model):
    news=models.ForeignKey(News,on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    body=models.TextField()
    created_on=models.DateTimeField(auto_now_add=True)
    active=models.BooleanField(default=True)
    comment_count = models.PositiveIntegerField(default=0)

    
    class Meta:
        ordering = ['created_on']
    
    def __str__(self):
        return f'Comment {self.pk}: {self.body[:30]!s}'


class NewsView(models.Model):

    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='views')
    ip_address = models.CharField(max_length=45)  # supports IPv6
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('news', 'ip_address')
        ordering = ['-created_on']

    def __str__(self):
        return f'{self.ip_address} -> {self.news_id}'