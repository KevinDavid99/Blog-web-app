from django.urls import path
from.views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView
from.import views


urlpatterns = [
    path('', PostListView.as_view() , name='home'),
    path('user/<str:username>',UserPostListView.as_view(), name = 'user-posts'),
    path('about/', views.about_page, name='about'),
    path('announce/', views.announcement, name='more'),
    path('post/<int:pk>/', PostDetailView.as_view() , name='post-detail'),
    path('post/new/', PostCreateView.as_view() , name='post-create'),
    path('post/<int:pk>/update',PostUpdateView.as_view(), name = 'post-update'),
    path('post/<int:pk>/delete',PostDeleteView.as_view(), name = 'post-delete'),
    # path('post/<int:pk>/delete',PostCommentDeleteView.as_view(), name = 'post-comment-delete'),
]