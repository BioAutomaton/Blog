from django.urls import path
from .views import HomeView, PostDetailView, CreatePostView, UpdatePostView, DeletePostView, UserProfileView, \
    CategoryView, CategoriesListView, DeleteCommentView

urlpatterns = [
    path('posts/', HomeView, name='home'),
    path('posts/add/', CreatePostView, name='add_post'),
    path('posts/<int:pk>/', PostDetailView, name='post_details'),
    path('posts/<int:pk>/edit', UpdatePostView, name='edit_post'),
    path('posts/<int:pk>/delete', DeletePostView, name='delete_post'),
    path('profile/<int:pk>', UserProfileView, name='profile'),
    path('posts/categories', CategoriesListView.as_view(), name='categories'),
    path('posts/categories/<int:pk>', CategoryView, name='category'),
    path('comments/<int:pk>/delete', DeleteCommentView, name='delete_comment')
]
