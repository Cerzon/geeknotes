from rest_framework.viewsets import ModelViewSet

from .models import GeekUser
from .serializers import GeekUserModelSerializer


class GeekUserModelViewSet(ModelViewSet):
    queryset = GeekUser.objects.all()
    serializer_class = GeekUserModelSerializer
