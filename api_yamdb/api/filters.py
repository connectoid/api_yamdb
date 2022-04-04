from django_filters import rest_framework as filters

from reviews.models import Title


class FilterTitle(filters.FilterSet):
    genre = filters.CharFilter(field_name='genre__slug')
    category = filters.CharFilter(field_name='category__slug')
    year = filters.NumberFilter(field_name='year')
    name = filters.CharFilter(field_name='name', lookup_expr='startswith')

    class Meta:
        model = Title
        fields = ('genre', 'category', 'year', 'name',)
