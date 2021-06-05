from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings


class PostManager(models.Manager):
    def like_toggle(self, member, post_obj):
        if member in post_obj.liked.all():
            is_liked = False
            post_obj.liked.remove(member)
        else:
            is_liked = True
            post_obj.liked.add(member)
        return is_liked


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(blank=True,null=True,upload_to='post_image')
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True,null=True)
    # description = models.TextField(blank=True,null=True)
    liked = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name='liked')
    date_posted = models.DateTimeField(default=timezone.now)

    objects = PostManager()

    class Meta:
        ordering = ('-date_posted', )

    def __str__(self):
        return f' {self.title} ของ {self.author}' 

    def get_absolute_url(self):
        # return reverse('/post/{self.pk}/', kwargs={'pk': self.pk})
        return reverse('post_detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(blank=True,null=True)
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=True)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse("post_list")

    def __str__(self):
        return self.text