from rest_framework.serializers import (ModelSerializer,
                                        StringRelatedField)

from usersapp.serializers import GeekUserModelSerializer
from .models import Project, Note


class ProjectModelSerializer(ModelSerializer):
    users = StringRelatedField(many=True)

    class Meta:
        model = Project
        fields = '__all__'


class NoteModelSerializer(ModelSerializer):
    author = GeekUserModelSerializer()

    class Meta:
        model = Note
        fields = '__all__'
