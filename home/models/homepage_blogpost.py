# from django.db import models
# from modelcluster.fields import ParentalKey
# from wagtail.api import APIField
# from wagtail.models import Orderable
# from wagtailautocomplete.edit_handlers import AutocompletePanel

# from home.models import HomePage


# class HomePageBlogPost(Orderable):
#     """
#     Orderable association model for highlighted blog posts on homepage.
#     Replaces ParentalManyToManyField to avoid translation issues.
#     """

#     page = ParentalKey(
#         HomePage,
#         on_delete=models.CASCADE,
#         related_name="highlighted_blog_posts",
#         null=True,
#         blank=False,
#     )

#     blog_post = models.ForeignKey(
#         BlogPostPage,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=False,
#         verbose_name="Blog Post",
#         help_text="Select blog posts to highligt on homepage",
#     )

#     panels = [AutocompletePanel("blog_post", target_model=BlogPostPage)]

#     def __str__(self) -> str:
#         return self.blog_post.title
