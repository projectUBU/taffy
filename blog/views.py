from .models import Post, Comment
from app.models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PostForm,CommentForm
from django.views.generic import (
    ListView, DetailView,  View
)
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView
)

from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class PostView(View):
    models_comment_class = Comment
    models_class = Post
    form_class = PostForm
    initial = {'key': 'value'}
    template_name = 'blog/blog_index.html'
    success_url = '/blog/'
    
    
    def render(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)

    def get(self, request, *args, **kwargs):
        self.form = self.form_class(initial=self.initial) 
        try:
            self.keyword = self.request.GET['q']
        except:
            self.keyword = ''
        if (self.keyword != ''):
            self.post = self.models_class.objects.filter(
                Q(content__icontains=self.keyword) | Q(title__icontains=self.keyword) | Q(author__username__icontains=self.keyword))
        else:
            self.post = self.models_class.objects.all()
        
        page = request.GET.get('page', 1)
        paginator = Paginator(self.post, 10)
        try:
            self.posts = paginator.page(page)
        except PageNotAnInteger:
            self.posts = paginator.page(1)
        except EmptyPage:
            self.posts = paginator.page(paginator.num_pages)


        self.context = {
            'form':self.form,
            'posts':self.posts,
            
        }
        return self.render(request)
    
   
    def post(self, request, *args, **kwargs):
 
        self.form = self.form_class(request.POST, request.FILES)
        if self.form.is_valid():
            
            self.form.instance.author = self.request.user
            self.form.save()
            messages.success(
                request, ' created success!')
            return redirect(self.success_url)
           
        else:
            self.form = self.form_class(instance=self.request.user)
        self.context = {'form':self.form}
        return self.render(request)
        
class DetailPostView(LoginRequiredMixin,View):
    models_class = Post
    models_comment_class =Comment
    form_class = CommentForm
    initial = {'key': 'value'}
    template_name = 'blog/detail.html'



    def render(self, request,pk, *args, **kwargs):
        return render(request, self.template_name, self.context)

    def get(self, request, pk,*args, **kwargs):
        self.form = self.form_class(initial=self.initial)
        self.post = self.models_class.objects.filter(pk=pk)
        self.comment = self.models_comment_class.objects.filter(post__id=pk).order_by("-created_date")
        
        self.context = {'form':self.form,'posts':self.post,'comments':self.comment}
        return self.render(request,pk)

    def post(self, request, pk, *args, **kwargs):
        self.post = self.models_class.objects.get(pk=pk)
        self.form = self.form_class(request.POST)
        if self.form.is_valid():
            self.form.instance.author = self.request.user
            self.form.instance.post = self.post
            self.form.save()
            messages.success(
                request, f'You have successfully commented.')
            return redirect('post_detail' , pk)
        else:
            messages.info(request,"Something wrong")
        
        self.context={'form':self.form}
        return self.render(request,pk)
        
        

class DeleteCommentView(LoginRequiredMixin,View):
    models_class = Comment
    models_post_class = Post
    

    def get(self, request, pk,*args, **kwargs):
        self.comment = self.models_class.objects.get(pk=pk)
        print(self.comment.post.id)
        if self.request.user == self.comment.author:
            self.models_class.objects.filter(pk=pk).delete()
            messages.success(request, 'delete CM success!')
            return redirect('post_detail',self.comment.post.id)
        messages.warning(request, 'คุณเป็นใคร')
        return redirect('post_detail',self.comment.post.id)
        
    

class DeletePostView(LoginRequiredMixin,View):
    models_class = Post
    success_url = '/blog/'

    def redirect(self, request,pk, *args, **kwargs):
        return redirect(self.success_url)

    def get(self, request, pk,*args, **kwargs):
        self.post = self.models_class.objects.get(pk=pk)
        print(self.post)
        if self.request.user == self.post.author:
            self.models_class.objects.filter(pk=pk).delete()
            messages.success(request, 'delete success!')
            return self.redirect(self, request,pk)
        messages.warning(request, 'คุณเป็นใครจะมาลบของฉัน')
        return self.redirect(self, request,pk)
        

class UpdatePostView(LoginRequiredMixin,View):
    models_class = Post
    success_url = "/blog/"
    form_class = PostForm
    template_name = 'blog/update.html'
    initial = {'key': 'value'}

    def redirect(self, request,pk, *args, **kwargs):
        return redirect(self.success_url)
        
    def render(self, request,pk, *args, **kwargs):
        return render(request, self.template_name, self.context)

    def get(self, request,pk, *args, **kwargs):
        self.post =self.models_class.objects.get(pk=pk)
        if self.request.user == self.post.author:
            self.form = self.form_class(instance=self.post)
        else:
            messages.info(request, "ของคนอื่นแก้ไม่ได้")
            return self.redirect(request,pk)
        self.context = {'form':self.form,'posts':self.post}
        return self.render(request, pk)

    def post(self, request,pk,*args, **kwargs):
        self.post =self.models_class.objects.get(pk=pk)
        if self.request.user == self.post.author:
            self.form = PostForm( request.POST, request.FILES, instance=self.post)
            if self.form.is_valid():
                self.form.instance.author = self.request.user
                self.form.save()
                messages.success(request, "Your account has been updated!")
                return self.redirect(request,pk)
            else:
                messages.success(request, "จะไปแก้ของคนอื่นได้ไง")
           
        else:
            self.form = PostForm( instance=self.post)
           
        self.context = {'form':self.form}
        return self.render(request,pk)

class MemberPostListView(LoginRequiredMixin,View):
    models_class = Member
    models_post_class =Post
    models_coment_class = Comment
    template_name = 'blog/member_posts.html'
    paginate_by = 5

    def render(self, request,username,*args,**kwargs):
        return render(request, self.template_name, self.context)
        
    def get(self, request,username,*args, **kwargs):
        self.member = get_object_or_404(self.models_class,username=username)
        self.post = self.models_post_class.objects.filter(author=self.member).order_by("-date_posted")
        self.comment = self.models_coment_class.objects.filter(author=self.member)
        # print(self.post[0].liked)
        self.context = {'member':self.member,'posts':self.post,'comments':self.comment}
        return self.render(request,username)





class PostDetailView(DetailView):
    model = Post




def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})