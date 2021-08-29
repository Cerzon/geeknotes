from rest_framework.viewsets import ModelViewSet

from .models import Project, Note
from .serializers import ProjectModelSerializer, NoteModelSerializer


class ProjectModelViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectModelSerializer


class NoteModelViewSet(ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteModelSerializer
