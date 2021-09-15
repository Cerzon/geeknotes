import json
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from usersapp.models import GeekUser
from usersapp.views import GeekUserModelViewSet


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
BUNCH_OF_OBJECTS = [
    {
        'username': 'john_travolta',
        'first_name': 'John',
        'last_name': 'Travolta',
        'email': 'j_travolta@hollywood.com'
    },
    {
        'username': 'steve_buscemi',
        'first_name': 'Steve',
        'last_name': 'Buscemi',
        'email': 's_buscemy@usa.net'
    },
    {
        'username': 'tim_roth',
        'first_name': 'Tim',
        'last_name': 'Roth',
        'email': 't_roth@monsieur-hotel.com'
    }
]
SINGLE_OBJECT = {
    'username': 'quentin_tarantino',
    'first_name': 'Quentin',
    'last_name': 'Tarantino',
    'email': 'director@pulp-fiction.movie'
}
PARTIAL_OBJECT = {
    'first_name': 'Timothy',
    'last_name': 'Smith'
}


class TestGeekUserModelViewSet(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(**USER_DATA)
        GeekUser.objects.bulk_create([
            GeekUser(**data) for data in BUNCH_OF_OBJECTS
        ])
        self.content_type = Q(
            content_type=ContentType.objects.get_for_model(GeekUser)
        )
        self.list_url = '/api/users/'

    def test_api_get_list_by_anonymous(self):
        request_factory = APIRequestFactory()
        request = request_factory.get(self.list_url)
        view = GeekUserModelViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_get_list_by_user_without_permissions(self):
        request_factory = APIRequestFactory()
        request = request_factory.get(self.list_url)
        view = GeekUserModelViewSet.as_view({'get': 'list'})
        force_authenticate(request, self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_get_list_by_user_with_permission(self):
        request_factory = APIRequestFactory()
        request = request_factory.get(self.list_url)
        view = GeekUserModelViewSet.as_view({'get': 'list'})
        self.user.user_permissions.set(
            Permission.objects.filter(self.content_type, VIEW)
        )
        force_authenticate(request, self.user)
        response = view(request)
        response.render()
        self.assertEqual(
            (response.status_code, json.loads(response.content)),
            (
                status.HTTP_200_OK,
                {
                    'count': 4,
                    'next': None,
                    'previous': None,
                    'results': [USER_DATA, *BUNCH_OF_OBJECTS]
                }
            )
        )

    def test_api_get_retrieve_by_anonymous(self):
        pk = 2
        request_factory = APIRequestFactory()
        request = request_factory.get(f'{self.list_url}{pk}/')
        view = GeekUserModelViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=pk)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_get_retrieve_by_user_without_permissions(self):
        pk = 2
        request_factory = APIRequestFactory()
        request = request_factory.get(f'{self.list_url}{pk}/')
        view = GeekUserModelViewSet.as_view({'get': 'retrieve'})
        force_authenticate(request, self.user)
        response = view(request, pk=pk)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_get_retrieve_by_user_with_permission(self):
        pk = 2
        request_factory = APIRequestFactory()
        request = request_factory.get(f'{self.list_url}{pk}/')
        view = GeekUserModelViewSet.as_view({'get': 'retrieve'})
        self.user.user_permissions.set(
            Permission.objects.filter(self.content_type, VIEW)
        )
        force_authenticate(request, self.user)
        response = view(request, pk=pk)
        response.render()
        self.assertEqual(
            (
                response.status_code,
                json.loads(response.content)
            ),
            (
                status.HTTP_200_OK,
                BUNCH_OF_OBJECTS[0]
            )
        )

    def test_api_post_create_by_anonymous(self):
        request_factory = APIRequestFactory()
        request = request_factory.post(self.list_url, SINGLE_OBJECT)
        view = GeekUserModelViewSet.as_view({'post': 'create'})
        with self.assertRaisesMessage(
            expected_exception=AttributeError,
            expected_message="'GeekUserModelViewSet' object has no attribute 'create'"
        ):
            view(request)

    def test_api_post_create_by_user_without_permissions(self):
        request_factory = APIRequestFactory()
        request = request_factory.post(self.list_url, SINGLE_OBJECT)
        view = GeekUserModelViewSet.as_view({'post': 'create'})
        force_authenticate(request, self.user)
        with self.assertRaisesMessage(
            expected_exception=AttributeError,
            expected_message="'GeekUserModelViewSet' object has no attribute 'create'"
        ):
            view(request)

    def test_api_post_create_by_user_with_permission(self):
        request_factory = APIRequestFactory()
        request = request_factory.post(self.list_url, SINGLE_OBJECT)
        view = GeekUserModelViewSet.as_view({'post': 'create'})
        self.user.user_permissions.set(
            Permission.objects.filter(self.content_type, ADD)
        )
        force_authenticate(request, self.user)
        with self.assertRaisesMessage(
            expected_exception=AttributeError,
            expected_message="'GeekUserModelViewSet' object has no attribute 'create'"
        ):
            view(request)

    def test_api_put_update_by_anonymous(self):
        pk = 2
        request_factory = APIRequestFactory()
        request = request_factory.put(f'{self.list_url}{pk}/', SINGLE_OBJECT)
        view = GeekUserModelViewSet.as_view({'put': 'update'})
        response = view(request, pk=pk)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_put_update_by_user_without_permissions(self):
        pk = 2
        request_factory = APIRequestFactory()
        request = request_factory.put(f'{self.list_url}{pk}/', SINGLE_OBJECT)
        view = GeekUserModelViewSet.as_view({'put': 'update'})
        force_authenticate(request, self.user)
        response = view(request, pk=pk)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_put_update_by_user_with_permission(self):
        pk = 2
        request_factory = APIRequestFactory()
        request = request_factory.put(f'{self.list_url}{pk}/', SINGLE_OBJECT)
        view = GeekUserModelViewSet.as_view({'put': 'update'})
        self.user.user_permissions.set(
            Permission.objects.filter(self.content_type, CHANGE)
        )
        force_authenticate(request, self.user)
        response = view(request, pk=pk)
        response.render()
        self.assertEqual(
            (
                response.status_code,
                json.loads(response.content)
            ),
            (
                status.HTTP_200_OK,
                SINGLE_OBJECT
            )
        )

    def test_api_patch_update_by_anonymous(self):
        pk = 4
        request_factory = APIRequestFactory()
        request = request_factory.patch(f'{self.list_url}{pk}/', PARTIAL_OBJECT)
        view = GeekUserModelViewSet.as_view({'patch': 'partial_update'})
        response = view(request, pk=pk)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_patch_update_by_user_without_permissions(self):
        pk = 4
        request_factory = APIRequestFactory()
        request = request_factory.patch(f'{self.list_url}{pk}/', PARTIAL_OBJECT)
        view = GeekUserModelViewSet.as_view({'patch': 'partial_update'})
        force_authenticate(request, self.user)
        response = view(request, pk=pk)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_patch_update_by_user_with_permission(self):
        pk = 4
        request_factory = APIRequestFactory()
        request = request_factory.patch(f'{self.list_url}{pk}/', PARTIAL_OBJECT)
        view = GeekUserModelViewSet.as_view({'patch': 'partial_update'})
        self.user.user_permissions.set(
            Permission.objects.filter(self.content_type, CHANGE)
        )
        force_authenticate(request, self.user)
        response = view(request, pk=pk)
        response.render()
        self.assertEqual(
            (
                response.status_code,
                json.loads(response.content)
            ),
            (
                status.HTTP_200_OK,
                BUNCH_OF_OBJECTS[~0] | PARTIAL_OBJECT
            )
        )

    def test_api_delete_destroy_by_anonymous(self):
        pk = 4
        request_factory = APIRequestFactory()
        request = request_factory.delete(f'{self.list_url}{pk}/')
        view = GeekUserModelViewSet.as_view({'delete': 'destroy'})
        with self.assertRaisesMessage(
            expected_exception=AttributeError,
            expected_message="'GeekUserModelViewSet' object has no attribute 'destroy'"
        ):
            view(request, pk=pk)

    def test_api_delete_destroy_by_user_without_permissions(self):
        pk = 4
        request_factory = APIRequestFactory()
        request = request_factory.delete(f'{self.list_url}{pk}/')
        view = GeekUserModelViewSet.as_view({'delete': 'destroy'})
        force_authenticate(request, self.user)
        with self.assertRaisesMessage(
            expected_exception=AttributeError,
            expected_message="'GeekUserModelViewSet' object has no attribute 'destroy'"
        ):
            view(request, pk=pk)

    def test_api_delete_destroy_by_user_with_permission(self):
        pk = 4
        request_factory = APIRequestFactory()
        request = request_factory.delete(f'{self.list_url}{pk}/')
        view = GeekUserModelViewSet.as_view({'delete': 'destroy'})
        self.user.user_permissions.set(
            Permission.objects.filter(self.content_type, DELETE)
        )
        force_authenticate(request, self.user)
        with self.assertRaisesMessage(
            expected_exception=AttributeError,
            expected_message="'GeekUserModelViewSet' object has no attribute 'destroy'"
        ):
            view(request, pk=pk)
