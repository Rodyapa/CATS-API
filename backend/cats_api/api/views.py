from rest_framework import viewsets, mixins
from cats.models import Breed
from api.permissions import IsStaffOrReadonly
from api.serializers import BreedSerializer


class BreedViewSet(mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    """
    View set that process requests related to cats instances.

    - Get list of all instances
    - Create a new breed instance (Only for Staff Users)
    - Delete a specific breed instance (Only for Staff Users)
    - Replace a specific breed instance  (Only for Staff Users)
    """

    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    permission_classes = (IsStaffOrReadonly, )
    http_method_names = ['get', 'post', 'put', 'delete']
