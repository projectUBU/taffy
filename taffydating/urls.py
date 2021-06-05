
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from app import views as member_views
from chat import tests
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Taffy ADMIN urls
    path('admin/', admin.site.urls),

    # app urls
    path('', include('app.urls')),

    # taffy Blog urls
    path('blog/', include('blog.urls')),

  
    # Chat urls
    path('dm/', include('chat.urls')),
   

    # Members urls for tests.py
    path('test/', tests.Test.as_view(), name='match'),
    # path('<int:pk>/like/',tests.LikeTest.as_view(), name='like'),
    # path('<int:pk>/nope/',tests.NopeTest.as_view(), name='nope'),





    # API urls

    path('api-taffy/', include('blog.api.urls')),
    path('api-blog/', include('blog.api.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),



    # Authentication Urls

    path('register/', member_views.RegisterView.as_view(
        template_name='app/register.html'), name='register'),
    path('login/', member_views.LoginView.as_view(
        template_name='app/wellcome.html'), name='login'),
    path('logout/', member_views.logout_views, name='logout'),
    path('profile/', member_views.ProfileView.as_view(),name='profile'),

 
    # Resete Password Urls

    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='app/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='app/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='app/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete', auth_views.PasswordResetCompleteView.as_view(
        template_name='app/password_reset_complete.html'), name='password_reset_complete'),
    # Change Password Urls
    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='app/password_change.html'), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='app/password_change_done.html'), name='password_change_done'),
]

if settings.DEBUG:
    # import debug_toolbar
    # urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
