from django.db.models import SET_NULL, ForeignKey
from wagtail.admin.panels import FieldPanel, ObjectList, TabbedInterface
from wagtail.models import Page


class BlogIndexPage(Page):
    """
    Index page for blog posts.
    Used for nesting blog posts under a single page.
    Allows highlighting a single blog post.
    """

    highlighted_post = ForeignKey(
        "blog.BlogPostPage",
        null=True,
        blank=True,
        on_delete=SET_NULL,
        related_name="+",
    )

    content_panels = [*Page.content_panels, FieldPanel("highlighted_post")]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Content"),
        ]
    )

    subpage_types = ["blog.BlogPostPage"]
    max_count = 1

    class Meta:
        verbose_name = "Blog Index"
        verbose_name_plural = "Blog Indexes"
