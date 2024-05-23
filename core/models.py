from datetime import datetime
from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField

User = get_user_model()


# Create your models here.

# Profile model
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.TextField(max_length = 255,blank=True)
    image = models.CharField(max_length = 255,default='https://res.cloudinary.com/dtq4d7luc/image/upload/v1710833246/default_gfiz3i.jpg')
    website = models.CharField(max_length = 255,blank=True)
    no_of_following = models.IntegerField(default=0)
    no_of_followed = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
    

# Post model
class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    caption = models.TextField(max_length=255,blank=True)
    create_at = models.DateTimeField(default=datetime.now)
    image = models.CharField(max_length=255)
    location = models.CharField(max_length=255,blank=True)
    no_of_like = models.IntegerField(default=0)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE, related_name = 'posts')

    def __str__(self):
        return self.user_id.username

# Like model
class Like(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)
    
    def __str__(self):
        return self.username

# Follow model
class Follow(models.Model):
    # user
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'followeds')
    # người user follow 
    following_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'followings')
    
    def __str__(self):
        return self.user.username

# Comment model
class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=255)
    create_at = models.DateTimeField(default=datetime.now)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name = 'comments')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    no_of_like = models.IntegerField(default=0)

    def __str__(self):
        return self.user_id.username
    
    
# Like comment model
class Comment_liked_by_user(models.Model):
    comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name = 'liked_comments')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user_id.username

# Hastag model
class Hastag(models.Model):
    hastag_id = models.AutoField(primary_key=True)
    hastag_name = models.CharField(max_length=50)

# Post_hastag model
class Post_hastag(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name = 'post_hastags')
    hastag_id = models.ForeignKey(Hastag, on_delete=models.CASCADE)

# Notification model
class Notification(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE, related_name='notifications_received')
    user_create = models.ForeignKey(User,on_delete=models.CASCADE,related_name='notifications_created')
    link = models.CharField(max_length=225,blank=True)
    type = models.CharField(max_length=20)
    created_at = models.DateTimeField(default=datetime.now)
    description = models.CharField(max_length=225, blank=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.user_id.username
    