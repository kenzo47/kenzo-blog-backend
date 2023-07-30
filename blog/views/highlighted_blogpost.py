from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from wagtail.models import Locale, Page

from blog.models import BlogIndexPage, BlogPostPage
from blog.serializers import BlogPostPageSerializer


@extend_schema(
    tags=["Blog"],
    parameters=[OpenApiParameter("locale", description="Locale string", type=str, required=True)],
    responses=BlogPostPageSerializer,
)
class HighlightedBlogPostPageAPIView(generics.RetrieveAPIView):
    """
    API endpoint to retrieve the highlighted blog post for a given locale.
    params:
        locale: Locale string
    """

    serializer_class = BlogPostPageSerializer

    def get_queryset(self) -> BlogPostPage:
        if "locale" not in self.request.query_params:
            raise ValidationError("Please provide a Locale.")
        locale = Locale.objects.get(language_code=self.request.query_params.get("locale"))
        try:
            blog_index_page = BlogIndexPage.objects.get(locale=locale).live().public()
            highlighted_post = blog_index_page.highlighted_post
        except Page.DoesNotExist as e:
            raise ValidationError("No highlighted blog post found") from e
        return highlighted_post
