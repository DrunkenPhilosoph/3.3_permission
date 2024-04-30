from django_filters import rest_framework as filters
from django_filters.filters import DateFromToRangeFilter
from advertisements.models import Advertisement

class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    # TODO: задайте требуемые фильтры
    date = DateFromToRangeFilter(field_name='created_at')

    class Meta:
        model = Advertisement
        fields = ['created_at']