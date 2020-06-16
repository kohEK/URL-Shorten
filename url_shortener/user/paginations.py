from rest_framework.pagination import CursorPagination


class MyPagination(CursorPagination):
    page_size = 3
    ordering = '-id'

# pagination 이 추가되면, users list에 results가 추가된다.***

