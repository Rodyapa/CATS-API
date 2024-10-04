from cats.models import Cat
from django_filters import rest_framework as filters


class CatFilter(filters.FilterSet):
    breed = filters.CharFilter(field_name='breed__name', lookup_expr='iexact')

    class Meta:
        model = Cat
        fields = ['breed']
