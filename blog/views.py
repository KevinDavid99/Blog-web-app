from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from.models import Post, CreateImages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 
from django.contrib.auth.models import User
from.forms import ImagesPost
from django.utils.text import Truncator
# Create your views here.

@login_required(login_url='login')
def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

@login_required(login_url='login')
def about_page(request):
    return render(request, 'blog/About.html')

def announcement(request):
    return render(request, 'blog/announcement.html')


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'[0:99]
    ordering = ['-date_posted']
    paginate_by = 4
    


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
        




class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

@login_required(login_url='login')
def create_image(request):
    if request.method == 'POST':
        form = ImagesPost(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        #     posts = CreateImages.objects.all()
            return redirect('pictures')
        # return render(request, 'hyperapp/upload_pics.html', {'img_posts':posts})
    else:
        form = ImagesPost()
    return render(request, 'blog/createimages_form.html', {'form':form})

@login_required(login_url='login')
def display_upload_pic(request):
    posts = CreateImages.objects.all()
    return render(request, 'blog/upload_pics.html', {'img_posts':posts})


# class PictureDetailView(DetailView):
#     model = CreateImages

# def like_post(request):
#     username = request.user.username
#     image_id = request.GET.get('image_id')

#     post = CreateImages.objects.get('image_id')

#     like_filter = LikePost.objects.filter(image_id=image_id, username=username)
#     if like_filter == None:
#         new_like = LikePost.objects.create(image_id=image_id, username=username)
#         new_like.save()
#         CreateImages.no_of_likes = CreateImages.no_of_likes+1
#         CreateImages.save()
#         return redirect('home')
#     else:
#         like_filter.delete()
#         CreateImages.no_of_likes = CreateImages.no_of_likes-1
#         CreateImages.save()
#         return redirect('home')

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self): # working with the UserPassesTestMixin, to prevent other users to update ur post
        post = self.get_object()
        if self.request.user == post.author: #getting the current user is the author of the post
            return True
        else:
            return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


class ImageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CreateImages
    success_url = '/'
    def test_func(self):
        image = self.get_object()
        if self.request.user == image:
            return True
        else:
            return False