from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from blog.forms import PostForm
from blog.models import Post


class LandingPageView(TemplateView):
    template_name = 'blog/landing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_posts'] = (
            Post.objects.select_related('author').order_by('-created_at')[:3]
        )
        return context


class BlogListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/blog_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.select_related('author').order_by('-created_at')


class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'blog/blog_detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'id'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Post.objects.select_related('author'),
            id=self.kwargs['id'],
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        user = self.request.user
        context['can_edit'] = user.is_staff or post.author == user
        context['can_delete'] = user.is_staff or post.author == user
        return context


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/blog_form.html'
    success_url = reverse_lazy('blog-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Write a New Post'
        context['submit_label'] = 'Publish'
        return context


class BlogEditView(LoginRequiredMixin, View):
    template_name = 'blog/blog_form.html'

    def get_post(self):
        post = get_object_or_404(
            Post.objects.select_related('author'),
            id=self.kwargs['id'],
        )
        if not (self.request.user.is_staff or post.author == self.request.user):
            raise PermissionDenied
        return post

    def get(self, request, *args, **kwargs):
        post = self.get_post()
        form = PostForm(instance=post)
        from django.shortcuts import render
        return render(request, self.template_name, {
            'form': form,
            'post': post,
            'form_title': 'Edit Post',
            'submit_label': 'Update',
        })

    def post(self, request, *args, **kwargs):
        post = self.get_post()
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog-detail', id=post.id)
        from django.shortcuts import render
        return render(request, self.template_name, {
            'form': form,
            'post': post,
            'form_title': 'Edit Post',
            'submit_label': 'Update',
        })


class BlogDeleteView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(
            Post.objects.select_related('author'),
            id=self.kwargs['id'],
        )
        if not (request.user.is_staff or post.author == request.user):
            raise PermissionDenied
        post.delete()
        return redirect('blog-list')