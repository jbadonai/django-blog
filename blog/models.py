from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import render, redirect


class PostCommentModel(models.Model):
    '''
        This is used for comments on each post
    '''
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_date = models.CharField(max_length=50)
    # comment_date = models.CharField(null=True, max_length=50)
    # comment_title = models.CharField(max_length=200, null=True)
    comment_title = models.CharField(max_length=200)
    comment = models.TextField()

    def __str__(self):
        return self.comment


class BlogModel(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date_posted = models.CharField(max_length=30)
    conversation = models.ForeignKey(PostCommentModel, on_delete=models.CASCADE, null=True)

    # post_comment = models.ForeignKey(PostCommentModel, on_delete=models.CASCADE, null=True)
    # post_comment = models.ForeignKey(PostCommentModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('home_page')



class CommentsModel(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return self.comment

