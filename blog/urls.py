from django.urls import path
from . import views
from .views import *



urlpatterns = [
   
    path('', PostView.as_view(), name='blog'),
    path('member/<str:username>/', MemberPostListView.as_view(), name='member_posts'),
    path('post/<int:pk>/', DetailPostView.as_view(), name='post_detail'),
    path('about/', views.about, name='about'),
    path('post/<int:pk>/update/', UpdatePostView.as_view(), name='post_update'),
    path('post/delete/<int:pk>/',DeletePostView.as_view(), name='delete_post'),
    path('comment/delete/<int:pk>/',DeleteCommentView.as_view(), name='delete_comment'),
    
    
]