from django.urls import  path
from . import views
urlpatterns = [
    # path('', views.home, name='home_page'),
    # path('', views.BlogListView.as_view(), name='home_page'),
    path('', views.blog_list_view, name='home_page'),

    path('register/', views.register, name='register'),
    # path('register/', views.Register.as_view(), name='register'),

    path('post/<int:pk>', views.blog_detail_view, name='post_details_page'),
    # path('post/<int:pk>', views.BlogDetailView.as_view(), name='post_details_page'),

    # path('post/new/', views.BlogCreateView.as_view(), name='post_new_page'),
    path('post/new/', views.blog_create_view, name='post_new_page'),

    path('post/<int:pk>/edit/', views.BlogUpdateView.as_view(), name='post_edit_page'),

    path('post/<int:pk>/delete/', views.BlogDeleteView.as_view(), name='post_delete_page')


]