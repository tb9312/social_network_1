from django.contrib import admin
from .models import Profile,Post,Like,Follow,Comment,Comment_liked_by_user,Hastag,Post_hastag,Notification
# Register your models here.

@admin.register(Profile)
class ProfileDisplay(admin.ModelAdmin):
    list_display = [field.name for field in Profile._meta.get_fields() if field.name != "id"]

class PostDisplay(admin.ModelAdmin):
    list_display=['caption','create_at','image','location','no_of_like','user_id']
admin.site.register(Post,PostDisplay)

@admin.register(Like)
class LikeDisplay(admin.ModelAdmin):
    list_display = [field.name for field in Like._meta.get_fields() if field.name != "id"]

@admin.register(Follow)
class FollowDisplay(admin.ModelAdmin):
    list_display = [field.name for field in Follow._meta.get_fields() if field.name != "id"]

class CommentDisplay(admin.ModelAdmin):
    list_display = ['content', 'create_at','post_id','user_id','no_of_like']
admin.site.register(Comment, CommentDisplay)

@admin.register(Comment_liked_by_user)
class LikeCommentDisplay(admin.ModelAdmin):
    list_display = [field.name for field in Comment_liked_by_user._meta.get_fields() if field.name != "id"]

@admin.register(Notification)
class NotificationDisplay(admin.ModelAdmin):
    list_display = [field.name for field in Notification._meta.get_fields() if field.name != "id"]

admin.site.register(Hastag)
admin.site.register(Post_hastag)