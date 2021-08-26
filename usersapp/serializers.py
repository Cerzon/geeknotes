from rest_framework.serializers import HyperlinkedModelSerializer
from .models import GeekUser


class GeekUserModelSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = GeekUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
        )
