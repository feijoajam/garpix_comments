import json
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType

from rest_framework import status
from rest_framework.test import APITestCase
from .models import Comment, Like


from testapp.models import MyPost

User = get_user_model()


class CommentTestCase(APITestCase):
    def setUp(self) -> None:
        self.password = '12345'
        self.username = 'test'
        self.username2 = 'test2'
        self.user1 = User.objects.create_user(username=self.username, email='user@site.com', password=self.password)
        self.user2 = User.objects.create_user(username=self.username2, email='user2@site.com', password=self.password)
        self.user3 = User.objects.create(username="test_username")
        self.model_type = ContentType.objects.get(model="mypost")

        self.post1 = MyPost.objects.create(name="post1", body="blah")
        self.post2 = MyPost.objects.create(name="post2", body="blahblah")

        self.comment1 = Comment.objects.create(object_id=self.post2.id, text="comm1", content_type=self.model_type, parent=None, author=self.user1)
        self.comment2 = Comment.objects.create(object_id=self.post2.id, text="comm2", content_type=self.model_type, parent=self.comment1, author=self.user1)
        self.comment3 = Comment.objects.create(object_id=self.post2.id, text="comm3", content_type=self.model_type, parent=self.comment1, author=self.user1)
        self.comment4 = Comment.objects.create(object_id=self.post2.id, text="comm4", content_type=self.model_type, parent=self.comment2, author=self.user1)

    def test_post_comment(self):
        url = reverse('garpix_comments:comments-list')
        comments_count = Comment.objects.all().count()
        self.client.force_login(self.user3)
        self.client.force_authenticate(self.user3)

        data = {
            "text": "comment1",
            "object_id": self.post1.pk,
            "content_type": self.model_type.id
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(comments_count + 1, Comment.objects.all().count())
        self.assertEqual(self.user3, Comment.objects.last().author)
        self.assertEqual(Comment.objects.last().source.pk, self.post1.pk)

    def test_depth_error(self):
        with self.assertRaisesMessage(ValidationError, "Максимальная вложенность: 3"):
            url = reverse('garpix_comments:comments-list')
            self.client.force_login(self.user3)
            self.client.force_authenticate(self.user3)
            data = {
                "text": "comment1",
                "object_id": self.post2.pk,
                "content_type": self.model_type.id,
                "parent": self.comment4.id
            }
            json_data = json.dumps(data)
            self.client.post(url, data=json_data, content_type='application/json')

    def test_model_error(self):
        with self.assertRaisesMessage(ValidationError, "Model comment must be in ACCEPTED_COMMENT_MODELS"):
            url = reverse('garpix_comments:comments-list')
            self.client.force_login(self.user3)
            self.client.force_authenticate(self.user3)
            data = {
                "text": "comment1",
                "object_id": self.comment1.pk,
                "content_type": ContentType.objects.get(model="comment").id,
                "parent": self.comment1.id
            }
            json_data = json.dumps(data)
            self.client.post(url, data=json_data, content_type='application/json')

    def test_no_source_error(self):
        url = reverse('garpix_comments:comments-list')
        self.client.force_login(self.user3)
        self.client.force_authenticate(self.user3)
        data = {
            "text": "comment1",
            "object_id": self.post2.pk + self.post1.pk,
            "content_type": self.model_type.id,
            "parent": self.comment1.id
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_wrong_source_error(self):
        with self.assertRaisesMessage(ValidationError, "Родитель и ребенок должны комментировать один объект"):
            url = reverse('garpix_comments:comments-list')
            self.client.force_login(self.user3)
            self.client.force_authenticate(self.user3)
            data = {
                "text": "comment1",
                "object_id": self.post1.pk,
                "content_type": self.model_type.id,
                "parent": self.comment1.id,
            }
            json_data = json.dumps(data)
            self.client.post(url, data=json_data, content_type='application/json')

    def test_like(self):
        url = reverse('garpix_comments:comments-like', args=(self.comment1.id,))
        json_data = json.dumps({})
        self.client.force_login(self.user1)
        self.client.force_authenticate(self.user1)

        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(Like.objects.filter(user=self.user1, comment=self.comment1).exists())
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertFalse(Like.objects.filter(user=self.user1, comment=self.comment1).exists())
