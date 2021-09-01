from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (ListModelMixin, RetrieveModelMixin,
                                    UpdateModelMixin)

from .models import GeekUser
from .serializers import GeekUserModelSerializer


class GeekUserModelViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    GenericViewSet,
):
    queryset = GeekUser.objects.all()
    serializer_class = GeekUserModelSerializer
