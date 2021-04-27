from django.test import TestCase
from .models import BlogModel
from django.contrib.auth import get_user_model
from django.urls import reverse


# Create your tests here.
class BlogTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@gmail.com',
            password='secret'
        )

        self.post = BlogModel.objects.create(
            title='A good title',
            body='Nice body',
            author=self.user
        )

    def test_string_representation(self):
        post = BlogModel(title='A simple title')
        self.assertEqual(str(post), post.title)

    def test_post_content(self):
        self.assertEqual(f"{self.post.title}", 'A good title')
        self.assertEqual(f"{self.post.author}", 'testuser')
        self.assertEqual(f"{self.post.body}", 'Nice body')

    def test_post_list_view(self):
        response = self.client.get(reverse('home_page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nice body')
        self.assertTemplateUsed(response, 'home.html')

    def test_post_details_views(self):
        response = self.client.get('/post/1/')
        no_response = self.client.get('/post/1000000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertTemplateUsed(response, 'post_details.html')



