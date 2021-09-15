from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination

from .models import Project, Note
from .serializers import (ProjectModelSerializerBase, ProjectModelSerializer,
                          NoteModelSerializerBase, NoteModelSerializer)
from .filters import ProjectInstancesFilter, NoteInstancesFilter


class ProjectPageNumberPagination(PageNumberPagination):
    page_size = 10


class ProjectModelViewSet(ModelViewSet):
    queryset = Project.objects.all()
    pagination_class = ProjectPageNumberPagination
    filterset_class = ProjectInstancesFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProjectModelSerializer
        return ProjectModelSerializerBase


class NotePageNumberPagination(PageNumberPagination):
    page_size = 20


class NoteModelViewSet(ModelViewSet):
    queryset = Note.objects.all()
    pagination_class = NotePageNumberPagination
    filterset_class = NoteInstancesFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return NoteModelSerializer
        return NoteModelSerializerBase

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
