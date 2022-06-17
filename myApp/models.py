from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class myUser(models.Model):

    myUserBase = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    blockedUsers = models.ManyToManyField(User, related_name="blocked_by", blank=True)

    def __str__(self):
        return self.myUserBase.__str__()

    def is_blocked(self, user):
        if self.blockedUsers.all().contains(user.myUserBase):
            return True
        return False


class Post(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(myUser, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to='specs', blank=True, null=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    onPost = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', default=1)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.author, self.onPost)


class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
