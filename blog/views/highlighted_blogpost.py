from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from wagtail.models import Locale, Page

from blog.models import BlogIndexPage, BlogPostPage
from blog.serializers import BlogPostPageSerializer


@extend_schema(
    tags=["Blog"],
    parameters=[OpenApiParameter("locale", description="Locale string", type=str, required=True)],
    responses=BlogPostPageSerializer,
)
class HighlightedBlogPostPageAPIView(APIView):
    """
    API endpoint to retrieve the highlighted blog post for a given locale.
    params:
        locale: Locale string
    """

    serializer_class = BlogPostPageSerializer

    def get(self, request) -> BlogPostPage:
        if "locale" not in self.request.query_params:
            raise ValidationError("Please provide a Locale.")
        locale = Locale.objects.get(language_code=self.request.query_params.get("locale"))
        try:
            blog_index_page = BlogIndexPage.objects.filter(locale=locale).first()
            highlighted_post = blog_index_page.highlighted_post if blog_index_page else None
            if not highlighted_post:
                raise Page.DoesNotExist
            return Response(self.serializer_class(highlighted_post).data)
        except Page.DoesNotExist as e:
            raise ValidationError("No highlighted blog post found.") from e
