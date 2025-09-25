import django_filters


class filter_trains(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    origin = django_filters.CharFilter(field_name='origin', lookup_expr='icontains')
    destination = django_filters.CharFilter(field_name='destination', lookup_expr='icontains')
    