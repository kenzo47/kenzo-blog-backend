from django.urls import path

from blog.views import BlogPostPageAPIView

app_name = "blog"

urlpatterns = [
    path("posts", BlogPostPageAPIView.as_view(), name="blog-post-list"),
]
