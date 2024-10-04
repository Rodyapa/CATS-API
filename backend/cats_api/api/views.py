from api.permissions import IsStaffOrReadonly
from api.serializers import BreedSerializer, CatSerializer
from api.filters import CatFilter
from cats.models import Breed, Cat
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class BreedViewSet(mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    """
    View set that process requests related to cats breed instances.

    - Get list of all instances
    - Create a new breed instance (Only for Staff Users)
    - Delete a specific breed instance (Only for Staff Users)
    - Replace a specific breed instance  (Only for Staff Users)
    """

    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    permission_classes = (IsStaffOrReadonly, )
    http_method_names = ['get', 'post', 'put', 'delete']


class CatsViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    """
    View set that process requests related to cats instances.

    - Get list of all instances
    - Get a specific cat instance
    - Create a new cat instance

    """

    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    http_method_names = ['get', 'post']
    filterset_class = CatFilter

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)