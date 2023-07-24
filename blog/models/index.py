from wagtail.models import Page


class BlogIndexPage(Page):
    """
    Index page for blog posts.
    Used for nesting blog posts under a single page.
    """

    subpage_types = ["blog.BlogPostPage"]
    max_count = 1

    class Meta:
        verbose_name = "Blog Index"
        verbose_name_plural = "Blog Indexes"
