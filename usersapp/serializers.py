from rest_framework.serializers import ModelSerializer
from .models import GeekUser


class GeekUserModelSerializer(ModelSerializer):
    class Meta:
        model = GeekUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
        )


class GeekUserModelSerializerV02(ModelSerializer):
    class Meta:
        model = GeekUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'is_staff',
            'is_superuser',
        )
