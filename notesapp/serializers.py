from rest_framework.serializers import (HyperlinkedModelSerializer,
                                        StringRelatedField,
                                        HyperlinkedRelatedField)

from usersapp.serializers import GeekUserModelSerializer
from .models import Project, Note


class ProjectModelSerializer(HyperlinkedModelSerializer):
    users = StringRelatedField(many=True)

    class Meta:
        model = Project
        fields = '__all__'


class NoteModelSerializer(HyperlinkedModelSerializer):
    project = HyperlinkedRelatedField(
        read_only=True,
        view_name='project-detail',
    )
    author = GeekUserModelSerializer()

    class Meta:
        model = Note
        fields = '__all__'
