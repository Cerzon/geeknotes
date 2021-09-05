from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination

from .models import Project, Note
from .serializers import ProjectModelSerializer, NoteModelSerializer
from .filters import ProjectInstancesFilter, NoteInstancesFilter


class ProjectPageNumberPagination(PageNumberPagination):
    page_size = 10


class ProjectModelViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectModelSerializer
    pagination_class = ProjectPageNumberPagination
    filterset_class = ProjectInstancesFilter


class NotePageNumberPagination(PageNumberPagination):
    page_size = 20


class NoteModelViewSet(ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteModelSerializer
    pagination_class = NotePageNumberPagination
    filterset_class = NoteInstancesFilter

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
