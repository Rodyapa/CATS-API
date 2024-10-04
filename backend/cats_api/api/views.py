from api.filters import CatFilter
from api.permissions import (IsAuthorOrIsStaffOrReadOnly,
                             IsOwnerOrIsStaffOrReadOnly, IsStaffOrReadonly)
from api.serializers import BreedSerializer, CatSerializer, ScoreSerializer
from cats.models import Breed, Cat, Score
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
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
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """
    View set that process requests related to cats instances.

    - Get list of all instances
    - Get a specific cat instance
    - Create a new cat instance

    """

    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = (IsOwnerOrIsStaffOrReadOnly, )
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    filterset_class = CatFilter

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Cat.objects.annotate(rating=Avg('scores__score'))


class ScoreViewSet(viewsets.ModelViewSet):
    """
    View set that process requests related to cats instances.

    - Add score to the specific cat
    - Edit score of the specific cat
    - Delete score of the specific cat
    - Get all scores of specific cat
    """

    serializer_class = ScoreSerializer
    http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorOrIsStaffOrReadOnly,
    )
    filter_backends = (filters.OrderingFilter,)
    ordering = ('pub_date',)

    def get_cat(self):
        cat = get_object_or_404(Cat, id=self.kwargs['cat_id'])
        return cat

    def get_queryset(self):
        return self.get_cat().scores.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            cat=self.get_cat()
        )

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'cat_id': self.kwargs['cat_id'],
        }
