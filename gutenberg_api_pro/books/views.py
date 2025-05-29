from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from .models import BooksBook
from .serializers import BookSerializer

class BookPagination(PageNumberPagination):
    """Custom pagination class to limit books per page."""

    page_size = 25


class BookListView(generics.ListAPIView):
    """
    API endpoint to retrieve a paginated list of books from Project Gutenberg.

    Query Parameters (all optional):
    - `book_id`: List of Gutenberg book IDs to filter by.
    - `language`: List of language codes (e.g., 'en', 'fr') to filter by.
    - `mime_type`: List of MIME types (e.g., 'text/plain', 'application/epub+zip') to filter by.
    - `topic`: List of keywords that match subjects or bookshelves.
    - `author`: Partial or full author name (case-insensitive).
    - `title`: Partial or full title (case-insensitive).
    - `page`: Page number for pagination (DRF handles this).
    """

    serializer_class = BookSerializer
    pagination_class = BookPagination

    allowed_filters = {
        "book_id",
        "language",
        "mime_type",
        "topic",
        "author",
        "title",
        "page",
    }

    book_id_param = openapi.Parameter(
        "book_id",
        openapi.IN_QUERY,
        description="Gutenberg book IDs (multiple allowed)",
        type=openapi.TYPE_ARRAY,
        items=openapi.Items(type=openapi.TYPE_INTEGER),
        required=False,
        collectionFormat="multi",
    )
    language_param = openapi.Parameter(
        "language",
        openapi.IN_QUERY,
        description="Language codes (e.g., 'en', 'fr')",
        type=openapi.TYPE_ARRAY,
        items=openapi.Items(type=openapi.TYPE_STRING),
        required=False,
        collectionFormat="multi",
    )
    mime_type_param = openapi.Parameter(
        "mime_type",
        openapi.IN_QUERY,
        description="MIME types (multiple allowed)",
        type=openapi.TYPE_ARRAY,
        items=openapi.Items(type=openapi.TYPE_STRING),
        required=False,
        collectionFormat="multi",
    )
    topic_param = openapi.Parameter(
        "topic",
        openapi.IN_QUERY,
        description="Topic keywords (match subjects or bookshelves)",
        type=openapi.TYPE_ARRAY,
        items=openapi.Items(type=openapi.TYPE_STRING),
        required=False,
        collectionFormat="multi",
    )
    author_param = openapi.Parameter(
        "author",
        openapi.IN_QUERY,
        description="Author name (partial or full, case-insensitive)",
        type=openapi.TYPE_STRING,
        required=False,
    )
    title_param = openapi.Parameter(
        "title",
        openapi.IN_QUERY,
        description="Book title (partial or full, case-insensitive)",
        type=openapi.TYPE_STRING,
        required=False,
    )
    page_param = openapi.Parameter(
        "page",
        openapi.IN_QUERY,
        description="Page number for pagination",
        type=openapi.TYPE_INTEGER,
        required=False,
    )

    @swagger_auto_schema(
        manual_parameters=[
            book_id_param,
            language_param,
            mime_type_param,
            topic_param,
            author_param,
            title_param,
            page_param,
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        """
        Build and return a filtered queryset based on supported query parameters.
        Raises ValidationError if any unknown query parameters are passed.
        """
        # Validate query parameters
        params = set(self.request.query_params.keys())
        invalid = params - self.allowed_filters
        if invalid:
            raise ValidationError(
                {
                    "detail": f"Invalid query parameters: {', '.join(invalid)}",
                    "allowed": list(self.allowed_filters),
                }
            )

        try:
            # Base queryset with related data optimized
            qs = BooksBook.objects.prefetch_related(
                "booksformat_set",
                "booksbookauthors_set__author",
                "booksbooksubjects_set__subject",
                "booksbooklanguages_set__language",
                "booksbookbookshelves_set__bookshelf",
            ).order_by("-download_count")

            # Filter by book IDs
            book_ids = self.request.query_params.getlist("book_id")
            if book_ids:
                qs = qs.filter(gutenberg_id__in=book_ids)

            # Filter by language codes
            languages = self.request.query_params.getlist("language")
            if languages:
                qs = qs.filter(booksbooklanguages__language__code__in=languages)

            # Filter by MIME types
            mime_types = self.request.query_params.getlist("mime_type")
            if mime_types:
                qs = qs.filter(booksformat__mime_type__in=mime_types)

            # Filter by topics (either in subjects or bookshelves)
            topics = self.request.query_params.getlist("topic")
            if topics:
                topic_q = Q()
                for topic in topics:
                    topic_q |= Q(booksbooksubjects__subject__name__icontains=topic)
                    topic_q |= Q(booksbookbookshelves__bookshelf__name__icontains=topic)
                qs = qs.filter(topic_q)

            # Filter by author name
            author = self.request.query_params.get("author")
            if author:
                qs = qs.filter(booksbookauthors__author__name__icontains=author)

            # Filter by book title
            title = self.request.query_params.get("title")
            if title:
                qs = qs.filter(title__icontains=title)
            
            return qs.distinct()

        except Exception as e:
            # Return user-friendly error on filter processing failure
            raise ValidationError(
                {"detail": f"An error occurred while filtering books: {str(e)}"}
            )