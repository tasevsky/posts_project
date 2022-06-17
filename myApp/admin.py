from django.contrib import admin
from .models import Post, Comment, myUser, PostComment


class MyUserAdmin(admin.ModelAdmin):
    list_display = ("myUserBase",)

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser or (obj and request.user == obj.user):
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False


class PostCommentAdmin(admin.StackedInline):
    model = PostComment
    extra = 0


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author")
    list_filter = ("created",)
    inlines = [PostCommentAdmin, ]

    def has_add_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        if obj and (request.user == obj.author):
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'onPost')

    def has_add_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        if (obj and (request.user == obj.author)) or (obj and request.user == obj.onPost.author):
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False


admin.site.register(myUser, MyUserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
