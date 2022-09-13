from django.urls import path
from.views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, ImageDeleteView
from.import views


urlpatterns = [
    path('', PostListView.as_view() , name='home'),
    path('user/<str:username>',UserPostListView.as_view(), name = 'user-posts'),
    path('about/', views.about_page, name='about'),
    path('announce/', views.announcement, name='more'),

    path('post/<int:pk>/', PostDetailView.as_view() , name='post-detail'),
    # path('images/<int:pk>/', PictureDetailView.as_view() , name='post-detail'),
    path('post/new/', PostCreateView.as_view() , name='post-create'),
    path('post/newpic/', views.create_image, name='post-new-pic'),
    path('post/<int:pk>/update',PostUpdateView.as_view(), name = 'post-update'),
    path('post/<int:pk>/delete',PostDeleteView.as_view(), name = 'post-delete'),
    path('image-delete/',ImageDeleteView.as_view(), name = 'image-delete'),
    path('images/', views.display_upload_pic, name='pictures'),

    # path('likepost/', views.like_post, name='like'),
    # path('images-delete/', views.delete_pic, name='images-delete'),

]