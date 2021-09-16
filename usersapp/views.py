from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (ListModelMixin, RetrieveModelMixin,
                                    UpdateModelMixin)

from .models import GeekUser
from .serializers import GeekUserModelSerializer, GeekUserModelSerializerV02


class GeekUserModelViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    GenericViewSet,
):
    queryset = GeekUser.objects.all()

    def get_serializer_class(self):
        if self.request.version == '0.2':
            return GeekUserModelSerializerV02
        return GeekUserModelSerializer
