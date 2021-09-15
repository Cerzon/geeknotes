from rest_framework.serializers import (ModelSerializer,
                                        StringRelatedField)

from usersapp.serializers import GeekUserModelSerializer
from .models import Project, Note


class ProjectModelSerializerBase(ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class ProjectModelSerializer(ProjectModelSerializerBase):
    users = StringRelatedField(many=True)


class NoteModelSerializerBase(ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'


class NoteModelSerializer(NoteModelSerializerBase):
    author = GeekUserModelSerializer()

