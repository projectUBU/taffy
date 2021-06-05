from django.urls import include,path
from rest_framework import routers
from .views import LikeToggleAPIView ,CommentViewSet
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'comment', CommentViewSet)

urlpatterns = [
    path('<int:pk>/like/', LikeToggleAPIView.as_view(), name='like_api'),
    path('', include(router.urls)),
   
   
]
