from django.urls import path

from blog.views import (
    BlogCreateView,
    BlogDeleteView,
    BlogDetailView,
    BlogEditView,
    BlogListView,
    LandingPageView,
)

urlpatterns = [
    path('', LandingPageView.as_view(), name='landing'),
    path('blogs/', BlogListView.as_view(), name='blog-list'),
    path('blog/<uuid:id>/', BlogDetailView.as_view(), name='blog-detail'),
    path('write/', BlogCreateView.as_view(), name='blog-create'),
    path('edit/<uuid:id>/', BlogEditView.as_view(), name='blog-edit'),
    path('delete/<uuid:id>/', BlogDeleteView.as_view(), name='blog-delete'),
]