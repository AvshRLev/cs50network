from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    follows_this_many = models.IntegerField(default=0)
    followed_by_this_many = models.IntegerField(default=0)


class Following(models.Model):
    user_followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_followed")
    followed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed_by")
    
    @classmethod
    def create(cls, user_followed, followed_by):
        followship = cls(user_followed=user_followed, followed_by=followed_by)
        return followship
    
    def __str__(self):
        return f"{self.user_followed} is followed by {self.followed_by}"




class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="poster")
    content = models.CharField(max_length=256)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.timestamp.date()} {str(self.timestamp.time())[0:5]} Post by {self.user}"
