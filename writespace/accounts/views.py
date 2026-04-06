from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView

from accounts.forms import CreateUserForm, LoginForm, RegisterForm
from blog.models import Post

import os


class LoginView(View):
    template_name = 'accounts/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return redirect('admin-dashboard')
            return redirect('blog-list')
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return redirect('admin-dashboard')
            return redirect('blog-list')
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_staff:
                    return redirect('admin-dashboard')
                return redirect('blog-list')
            else:
                form.add_error(None, 'Invalid username or password.')
        return render(request, self.template_name, {'form': form})


class RegisterView(View):
    template_name = 'accounts/register.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('blog-list')
        form = RegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('blog-list')
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                first_name=form.cleaned_data['display_name'],
            )
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('blog-list')
        return render(request, self.template_name, {'form': form})


class LogoutView(LoginRequiredMixin, View):

    def post(self, request):
        logout(request)
        return redirect('landing')


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_staff


class AdminDashboardView(StaffRequiredMixin, TemplateView):
    template_name = 'accounts/admin_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        thirty_days_ago = now - timezone.timedelta(days=30)

        total_posts = Post.objects.count()
        total_users = User.objects.count()
        admin_count = User.objects.filter(is_staff=True).count()
        recent_posts_count = Post.objects.filter(created_at__gte=thirty_days_ago).count()
        recent_posts = (
            Post.objects.select_related('author')
            .order_by('-created_at')[:5]
        )

        context.update({
            'total_posts': total_posts,
            'total_users': total_users,
            'admin_count': admin_count,
            'recent_posts_count': recent_posts_count,
            'recent_posts': recent_posts,
        })
        return context


class UserManagementView(StaffRequiredMixin, View):
    template_name = 'accounts/user_management.html'

    def get(self, request):
        users = User.objects.all().order_by('username')
        form = CreateUserForm()
        default_admin_username = os.environ.get('DEFAULT_ADMIN_USERNAME', 'admin')
        return render(request, self.template_name, {
            'users': users,
            'form': form,
            'default_admin_username': default_admin_username,
        })

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['display_name'],
            )
            if role == 'admin':
                user.is_staff = True
                user.save()
            messages.success(request, f'User "{user.username}" created successfully!')
            return redirect('user-management')

        users = User.objects.all().order_by('username')
        default_admin_username = os.environ.get('DEFAULT_ADMIN_USERNAME', 'admin')
        return render(request, self.template_name, {
            'users': users,
            'form': form,
            'default_admin_username': default_admin_username,
        })

    def delete(self, request, user_id):
        default_admin_username = os.environ.get('DEFAULT_ADMIN_USERNAME', 'admin')

        try:
            user_to_delete = User.objects.get(id=user_id)
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('user-management')

        if user_to_delete.username == default_admin_username:
            messages.error(request, 'Cannot delete the default admin user.')
            return redirect('user-management')

        if user_to_delete == request.user:
            messages.error(request, 'You cannot delete your own account.')
            return redirect('user-management')

        username = user_to_delete.username
        user_to_delete.delete()
        messages.success(request, f'User "{username}" deleted successfully!')
        return redirect('user-management')


class UserDeleteView(StaffRequiredMixin, View):

    def post(self, request, user_id):
        default_admin_username = os.environ.get('DEFAULT_ADMIN_USERNAME', 'admin')

        try:
            user_to_delete = User.objects.get(id=user_id)
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('user-management')

        if user_to_delete.username == default_admin_username:
            messages.error(request, 'Cannot delete the default admin user.')
            return redirect('user-management')

        if user_to_delete == request.user:
            messages.error(request, 'You cannot delete your own account.')
            return redirect('user-management')

        username = user_to_delete.username
        user_to_delete.delete()
        messages.success(request, f'User "{username}" deleted successfully!')
        return redirect('user-management')