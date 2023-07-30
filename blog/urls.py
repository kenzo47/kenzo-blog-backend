from django.urls import path

from blog.views import BlogPostPageAPIView, HighlightedBlogPostPageAPIView

app_name = "blog"

urlpatterns = [
    path("posts", BlogPostPageAPIView.as_view(), name="blog-post-list"),
    path("posts/highlighted", HighlightedBlogPostPageAPIView.as_view(), name="highlighted-blog-post"),
]
