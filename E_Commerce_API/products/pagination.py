from rest_framework.pagination import PageNumberPagination


class ProductPagination(PageNumberPagination):
    """
    Pagination for
    """

    page_size = 4  # Default page size
    page_query_param = "page"  # Default query parameter for page number
    page_size_query_param = "page_size"  # Default query parameter for page size
    max_page_size = 40  # Default max page size
