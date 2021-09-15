import json
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from mixer.backend.django import mixer

from notesapp.models import Project, Note


# settings for permission set
VIEW = Q(codename__startswith='view_')
ADD = Q(codename__startswith='add_')
CHANGE = Q(codename__startswith='change_')
DELETE = Q(codename__startswith='delete_')
# FULL = VIEW | ADD | CHANGE | DELETE

# data for create user to login
USER_DATA = {
    'username': 'shiny_and_fabulous',
    # 'password': 'realy_extra_complex_stuff',
    'email': 'zlaya@barabaka.su',
    'first_name': 'Shiny',
    'last_name': 'Fabulous',
}

# data for create a model instances
PROJECT_DATA = {
    'name': 'Also Sprach Zarathustra',
    'repo_url': 'http://localhost/zarathustra',
}
NOTE_DATA = {
    'is_active': True,
    'body': 'Reddite quae sunt Caesaris Caesari et quae sunt Dei Deo.'
}


class TestProjectModelViewSet(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(**USER_DATA)
        self.user_token = Token.objects.create(user=self.user)
        self.content_type = Q(
            content_type=ContentType.objects.get_for_model(Project)
        )
        self.list_url = '/api/projects/'
        mixer.cycle(3).blend(Project)
    
    def test_api_get_list_by_anonymous(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_get_list_by_user_without_permissions(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_get_list_by_user_with_permission(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        self.user.user_permissions.set(
            Permission.objects.filter(self.content_type, VIEW)
        )
        response = self.client.get(self.list_url)
        self.assertEqual(
            (response.status_code, json.loads(response.content)['count']),
            (status.HTTP_200_OK, len(Project.objects.all()))
        )
    
    def test_api_get_retrieve_by_anonymous(self):
        obj = mixer.blend(Project, **PROJECT_DATA)
        response = self.client.get(f'{self.list_url}{obj.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_get_retrieve_by_user_without_permissions(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        obj = mixer.blend(Project, **PROJECT_DATA)
        response = self.client.get(f'{self.list_url}{obj.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_get_retrieve_by_user_with_permission(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        self.user.user_permissions.set(
            Permission.objects.filter(self.content_type, VIEW)
        )
        obj = mixer.blend(Project, **PROJECT_DATA)
        response = self.client.get(f'{self.list_url}{obj.id}/')
        response_details = json.loads(response.content)
        self.assertEqual(
            (
                response.status_code,
                response_details['name'],
                response_details['repo_url']
            ),
            (
                status.HTTP_200_OK,
                PROJECT_DATA['name'],
                PROJECT_DATA['repo_url']
            )
        )
    
    def test_api_post_create_by_anonymous(self):
        response = self.client.post(
            self.list_url,
            PROJECT_DATA | {'users': [self.user.id]}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_post_create_by_user_without_permissions(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        response = self.client.post(
            self.list_url,
            PROJECT_DATA | {'users': [self.user.id]}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_post_create_by_user_with_permission(self):
        last_id = Project.objects.last().id
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        self.user.user_permissions.set(
            Permission.objects.filter(self.content_type, ADD)
        )
        response = self.client.post(
            self.list_url,
            PROJECT_DATA | {'users': [self.user.id]}
        )
        response_details = json.loads(response.content)
        self.assertEqual(
            (
                response.status_code,
                response_details['id'],
                response_details['name'],
                response_details['repo_url']
            ),
            (
                status.HTTP_201_CREATED,
                last_id + 1,
                PROJECT_DATA['name'],
                PROJECT_DATA['repo_url']
            )
        )

    def test_api_put_update_by_anonymous(self):
        obj = Project.objects.last()
        response = self.client.put(
            f'{self.list_url}{obj.id}/',
            PROJECT_DATA | {'users': [self.user.id]}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_put_update_by_user_without_permissions(self):
        obj = Project.objects.last()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        response = self.client.put(
            f'{self.list_url}{obj.id}/',
            PROJECT_DATA | {'users': [self.user.id]}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_put_update_by_user_with_permission(self):
        obj = Project.objects.last()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        self.user.user_permissions.set(
            Permission.objects.filter(self.content_type, CHANGE)
        )
        response = self.client.put(
            f'{self.list_url}{obj.id}/',
            PROJECT_DATA | {'users': [self.user.id]}
        )
        obj.refresh_from_db(fields=('name', 'repo_url'))
        self.assertEqual(
            (
                response.status_code,
                obj.name,
                obj.repo_url
            ),
            (
                status.HTTP_200_OK,
                PROJECT_DATA['name'],
                PROJECT_DATA['repo_url']
            )
        )

    def test_api_patch_update_by_anonymous(self):
        obj = Project.objects.last()
        response = self.client.patch(f'{self.list_url}{obj.id}/', PROJECT_DATA)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_patch_update_by_user_without_permissions(self):
        obj = Project.objects.last()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        response = self.client.patch(f'{self.list_url}{obj.id}/', PROJECT_DATA)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_patch_update_by_user_with_permission(self):
        obj = Project.objects.last()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        self.user.user_permissions.set(
            Permission.objects.filter(self.content_type, CHANGE)
        )
        response = self.client.patch(f'{self.list_url}{obj.id}/', PROJECT_DATA)
        obj.refresh_from_db(fields=('name', 'repo_url'))
        self.assertEqual(
            (
                response.status_code,
                obj.name,
                obj.repo_url
            ),
            (
                status.HTTP_200_OK,
                PROJECT_DATA['name'],
                PROJECT_DATA['repo_url']
            )
        )

    def test_api_delete_destroy_by_anonymous(self):
        obj = Project.objects.last()
        response = self.client.delete(f'{self.list_url}{obj.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_delete_destroy_by_user_without_permissions(self):
        obj = Project.objects.last()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        response = self.client.delete(f'{self.list_url}{obj.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_delete_destroy_by_user_with_permission(self):
        obj = Project.objects.last()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        self.user.user_permissions.set(
            Permission.objects.filter(self.content_type, DELETE)
        )
        response = self.client.delete(f'{self.list_url}{obj.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaisesMessage(
            expected_exception=Project.DoesNotExist,
            expected_message='Project matching query does not exist.'
        ):
            Project.objects.get(pk=obj.id)


class TestNoteModelViewSet(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(**USER_DATA)
        self.user_token = Token.objects.create(user=self.user)
        self.content_type = Q(
            content_type=ContentType.objects.get_for_model(Note)
        )
        self.list_url = '/api/notes/'
        mixer.cycle(5).blend(Note)
    
    def test_api_get_list_by_anonymous(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_get_list_by_user_without_permissions(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_get_list_by_user_with_permission(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        self.user.user_permissions.set(
            Permission.objects.filter(self.content_type, VIEW)
        )
        response = self.client.get(self.list_url)
        self.assertEqual(
            (response.status_code, json.loads(response.content)['count']),
            (status.HTTP_200_OK, len(Note.objects.all()))
        )
    
    def test_api_get_retrieve_by_anonymous(self):
        obj = mixer.blend(Note, **NOTE_DATA)
        response = self.client.get(f'{self.list_url}{obj.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_get_retrieve_by_user_without_permissions(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        obj = mixer.blend(Note, **NOTE_DATA)
        response = self.client.get(f'{self.list_url}{obj.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_get_retrieve_by_user_with_permission(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        self.user.user_permissions.set(
            Permission.objects.filter(self.content_type, VIEW)
        )
        obj = mixer.blend(Note, **NOTE_DATA)
        response = self.client.get(f'{self.list_url}{obj.id}/')
        response_details = json.loads(response.content)
        self.assertEqual(
            (
                response.status_code,
                response_details['is_active'],
                response_details['body']
            ),
            (
                status.HTTP_200_OK,
                NOTE_DATA['is_active'],
                NOTE_DATA['body']
            )
        )
    
    def test_api_post_create_by_anonymous(self):
        obj = Note.objects.last()
        response = self.client.post(
            self.list_url,
            NOTE_DATA | {'project': obj.project.id, 'author': obj.author.id}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_post_create_by_user_without_permissions(self):
        obj = Note.objects.last()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        response = self.client.post(
            self.list_url,
            NOTE_DATA | {'project': obj.project.id, 'author': obj.author.id}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_post_create_by_user_with_permission(self):
        obj = Note.objects.last()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        self.user.user_permissions.set(
            Permission.objects.filter(self.content_type, ADD)
        )
        response = self.client.post(
            self.list_url,
            NOTE_DATA | {'project': obj.project.id, 'author': obj.author.id}
        )
        response_details = json.loads(response.content)
        self.assertEqual(
            (
                response.status_code,
                response_details['id'],
                response_details['is_active'],
                response_details['body']
            ),
            (
                status.HTTP_201_CREATED,
                obj.id + 1,
                NOTE_DATA['is_active'],
                NOTE_DATA['body']
            )
        )

    def test_api_put_update_by_anonymous(self):
        obj = Note.objects.last()
        response = self.client.put(
            f'{self.list_url}{obj.id}/',
            NOTE_DATA | {'project': obj.project.id, 'author': obj.author.id}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_put_update_by_user_without_permissions(self):
        obj = Note.objects.last()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        response = self.client.put(
            f'{self.list_url}{obj.id}/',
            NOTE_DATA | {'project': obj.project.id, 'author': obj.author.id}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_put_update_by_user_with_permission(self):
        obj = Note.objects.last()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        self.user.user_permissions.set(
            Permission.objects.filter(self.content_type, CHANGE)
        )
        response = self.client.put(
            f'{self.list_url}{obj.id}/',
            NOTE_DATA | {'project': obj.project.id, 'author': obj.author.id}
        )
        obj.refresh_from_db(fields=('is_active', 'body'))
        self.assertEqual(
            (
                response.status_code,
                obj.is_active,
                obj.body
            ),
            (
                status.HTTP_200_OK,
                NOTE_DATA['is_active'],
                NOTE_DATA['body']
            )
        )

    def test_api_patch_update_by_anonymous(self):
        obj = Note.objects.last()
        response = self.client.patch(f'{self.list_url}{obj.id}/', NOTE_DATA)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_patch_update_by_user_without_permissions(self):
        obj = Note.objects.last()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        response = self.client.patch(f'{self.list_url}{obj.id}/', NOTE_DATA)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_patch_update_by_user_with_permission(self):
        obj = Note.objects.last()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        self.user.user_permissions.set(
            Permission.objects.filter(self.content_type, CHANGE)
        )
        response = self.client.patch(f'{self.list_url}{obj.id}/', NOTE_DATA)
        obj.refresh_from_db(fields=('is_active', 'body'))
        self.assertEqual(
            (
                response.status_code,
                obj.is_active,
                obj.body
            ),
            (
                status.HTTP_200_OK,
                NOTE_DATA['is_active'],
                NOTE_DATA['body']
            )
        )

    def test_api_delete_destroy_by_anonymous(self):
        obj = Note.objects.last()
        response = self.client.delete(f'{self.list_url}{obj.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_delete_destroy_by_user_without_permissions(self):
        obj = Note.objects.last()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        response = self.client.delete(f'{self.list_url}{obj.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_delete_destroy_by_user_with_permission(self):
        obj = Note.objects.last()
        obj.is_active = True
        obj.save()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        self.user.user_permissions.set(
            Permission.objects.filter(self.content_type, DELETE)
        )
        response = self.client.delete(f'{self.list_url}{obj.id}/')
        obj.refresh_from_db(fields=('is_active',))
        self.assertEqual(
            (response.status_code, obj.is_active),
            (status.HTTP_204_NO_CONTENT, False)
        )
