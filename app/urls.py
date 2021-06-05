

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from app import views as member_views
from app import tests
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', member_views.GetRatingView.as_view(), name='member_all'),
    path('match/', member_views.match, name='Match Page'),
    path('setting/', member_views.SettingsUpdateView.as_view(), name='setting'),
    path('<int:pk>/like/',member_views.LikeView.as_view(), name='like'),
    path('<int:pk>/nope/',member_views.NopeView.as_view(), name='nope'),
   
]
if settings.DEBUG:

    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

