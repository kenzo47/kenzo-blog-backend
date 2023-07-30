from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from wagtail.models import Locale

from blog.helpers import BlogPagination
from blog.models import BlogPostPage
from blog.serializers import BlogPostPageSerializer


@extend_schema(
    tags=["Blog"],
    parameters=[OpenApiParameter("locale", description="Locale string", type=str, required=True)],
    responses=BlogPostPageSerializer,
)
class BlogPostPageAPIView(generics.ListAPIView):
    """
    API endpoint to retrieve all blog posts for a given locale.
    params:
        locale: Locale string
        page_size: Number of results per page, defaults to 6
        ordering: Order the results by a field: created_at, updated_at, author
    """

    serializer_class = BlogPostPageSerializer
    pagination_class = BlogPagination
    ordering_fields = ["created_at", "updated_at", "author"]
    filter_backends = [OrderingFilter]

    def get_queryset(self) -> BlogPostPage:
        if "locale" not in self.request.query_params:
            raise ValidationError("Please provide a Locale.")
        locale = Locale.objects.get(language_code=self.request.query_params.get("locale"))
        try:
            blog_posts = BlogPostPage.objects.filter(locale=locale).live().public()
        except BlogPostPage.DoesNotExist as e:
            raise ValidationError("No blog posts found for this locale.") from e
        return blog_posts
