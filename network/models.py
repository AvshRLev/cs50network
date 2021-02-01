from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    follows_this_many = models.IntegerField(default=0)
    followed_by_this_many = models.IntegerField(default=0)
    # likes = models.ManyToManyField(Post, blank=True, related_name="users")

# class Like(models.Model):
#     user = models.ManyToManyField(User, blank=True, related_name="user_like")
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_liked")


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
    users_liking = models.ManyToManyField(User, blank=True, related_name="posts_liked")
    
    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "likes": self.likes,
        }

    def __str__(self):
        return f"post {self.id} by {self.user}"
