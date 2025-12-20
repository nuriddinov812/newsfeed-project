from django.db import models
from django.contrib.auth.models import AbstractUser, User

# Create your models here.

# class User(AbstractUser):
#     photo = models.ImageField()
#     date_of_birth = models.DateField()
#     adress = models.CharField(max_length=255)
    
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.FileField(upload_to='users/', blank=True, null=True, default='users/6596121.png')
    date_of_birth = models.DateField(blank=True,null=True)
    
    
    def __str__(self):
        return f'Profile {self.user.username}'
    