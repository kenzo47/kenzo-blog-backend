from django.conf import settings
from django.db.models import CASCADE, SET_NULL, DateTimeField, ForeignKey
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, ObjectList, TabbedInterface
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtailseo.models import SeoMixin, SeoType

from base.panels.seo import seo_panels


class BlogPostPage(SeoMixin, Page):
    """
    Model for blog posts.
    """

    category = ForeignKey(
        "blog.Category",
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name="Category",
        help_text="Choose a category for the blog post.",
    )
    image = ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        on_delete=SET_NULL,
        related_name="+",
        verbose_name="Image",
        help_text="Choose an image for the blog post.",
    )
    body = RichTextField(
        null=True,
        blank=True,
        verbose_name="body",
        help_text="Write your blog post content here.",
    )
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    author = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)

    content_panels = [
        *Page.content_panels,
        MultiFieldPanel(
            [FieldPanel("category"), FieldPanel("author"), FieldPanel("body")],
            heading="Blog post content",
        ),
    ]

    seo_panels = seo_panels(disable_slug=False)

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Content"),
            ObjectList(seo_panels, heading="SEO"),
        ]
    )

    subpage_types = []
    seo_content_type = SeoType.WEBSITE

    def seo_image(self) -> str:
        """
        Gets the primary Open Graph image of this page.
        """
        from base.models import SEOSetting

        if self.image:
            return self.image
        if self.og_image:
            return self.og_image
        seo_defaults = SEOSetting.objects.first()
        return seo_defaults.seo_image if seo_defaults else None

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Blog post"
        verbose_name_plural = "Blog posts"
