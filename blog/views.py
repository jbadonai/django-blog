from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, UpdateView, DeleteView,CreateView
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import RegistrationForm, CommentForm, NewBlogForm
from .models import BlogModel, CommentsModel, PostCommentModel
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django import  *
from django.urls import resolve, reverse, reverse_lazy
# FUNCTION TO HOME PAGE
from datetime import datetime

# https://docs.djangoproject.com/en/3.2/ref/templates/builtins/

def get_current_date_time():
    return  datetime.today().strftime('%d - %b, %Y  %H:%M%p')

def home(request):
    return render(request, 'home.html')


# CLASS BASE VIEW FOR VIEWING LIST OF BLOG AT HOME PAGE
class BlogListView(ListView):
    paginate_by = 5
    model = BlogModel
    template_name = 'home.html'


# FUNCTION BASE FOR VIEWING LIST OF BLOG AT HOME PAGE
def blog_list_view(response):
    object_list = BlogModel.objects.all()
    comment_list = CommentsModel.objects.all()
    comment_Model = CommentsModel
    cuser = response.user

    paginator = Paginator(object_list, 7)
    page_number = response.GET.get('page')
    page_obj =  paginator.get_page(page_number)

    if response.method == 'POST':
        print(response.POST)

        form = CommentForm(response.POST)
        if form.is_valid():
            new = CommentsModel(author=cuser, comment=form.cleaned_data['comment'])
            new.save()

        return redirect('/')
    else:
        form = CommentForm()

    return render(response, 'home.html', {
        "page_obj": page_obj,
        'object_list': object_list,
        'comment_list': comment_list,
        'form': form,
    })


# CLASS VIEW FOR REGISTER --- NOT WORKING FINE
class Register(CreateView, UserCreationForm):
    model = User
    template_name = 'register.html'
    fields = ['username', 'email', 'password']


# FUNCTION BASED VIEW FOR REGISTER
def register(response):
    if response.method == "POST":
        form = RegistrationForm(response.POST)
        if form.is_valid():
            form.save()
        return redirect('/login')
    else:
        form = RegistrationForm()

    return render(response, 'register.html', {'form': form})


# CLASS BASE VIEW FOR VIEWING DETAILS OF EACH BLOG
class BlogDetailView(DetailView):
    model = BlogModel
    template_name = 'post_details.html'


# FUNCTION BASE VIEW FOR VIEWING BLOG DETAILS OF EACH BLOG
def blog_detail_view(response, pk):
    post = BlogModel.objects.get(id=pk)
    user = response.user
    postComment = PostCommentModel.objects.all()
    counter = 0

    # get the total number of title that corresponds to the current title in the commment
    # to count the number of comment for the current blog
    for p in postComment:
        if p.comment_title == post.title:
            counter += 1

    if response.method == 'POST':
        form = CommentForm(response.POST)
        if form.is_valid():
            new = PostCommentModel(author=user, comment_date=get_current_date_time(), comment_title=post.title, comment=form.cleaned_data['comment'])
            new.save()

            # ??? newly mod delete if error
            post.conversation = new
            post.save()
            print(post.conversation)

            return redirect(f'/post/{pk}')
    else:
        form = CommentForm()


    return render(response, 'post_details.html', {
        'pk': pk,
        'post': post,
        'cuser': user,
        'form': form,
        'postComment': postComment,
        'counter': counter,

    })


# CLASS BASE VIEW FOR CREATING NEW POST
class BlogCreateView(CreateView):
    model = BlogModel
    template_name = 'post_new.html'
    fields = ['author', 'title', 'body']


# FUNCTION BASE VIEW FOR CREATING NEW POST
def blog_create_view(response):
    cuser = response.user

    if response.method == "POST":
        form = NewBlogForm(response.POST)
        if form.is_valid():

            new = BlogModel(title=form.cleaned_data['title'],
                            date_posted=get_current_date_time(),
                            author=cuser,
                            body=form.cleaned_data['body'])
            new.save()
            return redirect('/')
    else:
        form = NewBlogForm()

    return render(response, 'post_new.html', {
        'cuser': cuser,
        'form': form,
    })


# CLASS BASED VIEW USED FOR UPDATING / AFTER EDITING [ EDIT POST ]
class BlogUpdateView(UpdateView):
    model = BlogModel
    template_name = 'post_edit.html'
    fields = ['title', 'body']

    # def post(self, request, *args, **kwargs):
    #     return redirect('/')


class BlogDeleteView(DeleteView):
    model = BlogModel
    template_name = 'post_delete.html'
    success_url = reverse_lazy('home_page')
