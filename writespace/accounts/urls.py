from django.urls import path

from accounts.views import (
    AdminDashboardView,
    LoginView,
    LogoutView,
    RegisterView,
    UserDeleteView,
    UserManagementView,
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('admin-panel/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('users/', UserManagementView.as_view(), name='user-management'),
    path('users/delete/<int:pk>/', UserDeleteView.as_view(), name='user-delete'),
]