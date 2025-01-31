from django.contrib.auth.models import AbstractUser
from django.db import models


class Posts(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey("User", on_delete=models.CASCADE, related_name="post_owner")
    content = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now=True)

    def likes_count(self):
        return self.likes.count()
    
    def __str__(self):
        return f"Post by {self.owner.username}: {self.content[:50]}       {self.date}"
    
    def isLikedBy(self, user):
        return self.likes.filter(id=user.id).exists()


class User(AbstractUser):
    following = models.ManyToManyField("self", blank=True, related_name="followers", symmetrical=False)
    like = models.ManyToManyField(Posts, blank=True, related_name="likes")

    def followed_by_count(self):
        return self.followers.count()
    
    def following_count(self):
        return self.following.count()