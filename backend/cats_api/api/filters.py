from django_filters import rest_framework as filters
from cats.models import Cat


class CatFilter(filters.FilterSet):
    breed = filters.CharFilter(field_name='breed__name', lookup_expr='iexact')

    class Meta:
        model = Cat
        fields = ['breed']
