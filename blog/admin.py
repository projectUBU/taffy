
from django.contrib import admin
from .models import Post, Comment

from django import forms
# from .models import QuillPost


class PostAdmin(admin.ModelAdmin):

    list_display = ('id',  'author','title' ,'content','image',  'date_posted')
    list_display_links = ('id', 'author',)
    list_filter = ('author', 'date_posted')
    list_editable = ( 'title' ,'content','image', )
    search_fields = ( 'title','content' ,'author__username',)
    list_per_page = 20


admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'post','text',
                    'approved_comment', 'created_date')
    list_display_links = ('id',  'post')
    list_filter = ('author', 'created_date')
    list_editable = ('text',)
    search_fields = ('post__title','text')
    list_per_page = 20


admin.site.register(Comment, CommentAdmin)