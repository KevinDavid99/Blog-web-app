from http.client import HTTPResponse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from.models import Post, PostComment
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 
from django.contrib.auth.models import User
from django.utils.text import Truncator
from blog.forms import NewCommentForm
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
    paginate_by = 5
    


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
        



#getting the detail of the post
class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post

    #for the comment section
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        comments_connected = PostComment.objects.filter(post = self.get_object()).order_by('-date_posted')
        data['comments'] = comments_connected
        if self.request.user.is_authenticated:
            data['comment_form'] = NewCommentForm(instance = self.request.user)
        return data


    def post(self, request, *args, **kwargs):
        new_comment = PostComment(comment=request.POST.get('comment'), author=self.request.user, post = self.get_object())
        new_comment.save()
        messages.success(request, 'Your comment has been sucessfully submitted')
        return self.get(self, request, *args, **kwargs)

    
# def delete_comment(request, pk):
#     comment = PostComment.objects.get(id=pk)

#     if request.user != comment.user:
#         return HTTPResponse('<h2>You are not allowed to perform this action</h2>')

#     if request.method == 'POST':
#         comment.delete()
#         return redirect('post-detail')
#     return render(request, 'blog/delete.html', {'obj':comment})


#Creating posts
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


#Updating posts
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

#Deleting Posts
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False
