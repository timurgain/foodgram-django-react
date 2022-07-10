from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    """Custom paginator based on PageNumberPagination.
    It is mainly for overriding the page_size_query_param."""
    page_size_query_param = 'limit'
    page_query_param = 'page'
    page_size = 5
