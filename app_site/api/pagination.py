from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination


class PostLimitOffSetPagination(LimitOffsetPagination):
    """
        /api/catadores/?offset=3
    """
    default_limit = 10
    max_limit =10


class PostPageNumberPagination(PageNumberPagination):
    page_size = 10