from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.models import Orderable
from wagtailautocomplete.edit_handlers import AutocompletePanel

from blog.models import BlogPostPage, Category


class BlogPostPageCategory(Orderable):
    """
    Orderable association model for categories on a blog page.
    Replaces ParentalManyToManyField to avoid translation issues.
    """

    page = ParentalKey(
        BlogPostPage,
        on_delete=models.CASCADE,
        related_name="blog_post_categories",
        null=True,
        blank=False,
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name="Category",
        help_text="Select categories for the blog post.",
    )

    panels = [AutocompletePanel("category", target_model=Category)]

    def __str__(self) -> str:
        return self.category.name
