from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, ObjectList, TabbedInterface
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail_headless_preview.models import HeadlessPreviewMixin
from wagtailseo.models import SeoMixin, SeoType

from base.panels.seo import seo_panels


class HomePage(HeadlessPreviewMixin, SeoMixin, Page):
    """
    Home page model.
    All other pages are nested under this page.
    """

    # Hero section
    hero_title = models.CharField(max_length=100, blank=False, null=True)
    hero_subtitle = models.CharField(max_length=100, blank=True, null=True)
    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    # Main content section
    main_content = RichTextField(blank=True, null=True)

    # Contact section
    contact_title = models.CharField(max_length=100, blank=True, null=True)
    contact_subtitle = models.CharField(max_length=100, blank=True, null=True)
    contact_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = [
        *Page.content_panels,
        MultiFieldPanel(
            [FieldPanel("hero_title"), FieldPanel("hero_subtitle"), FieldPanel("hero_image")], heading="Hero section"
        ),
        FieldPanel("main_content"),
        MultiFieldPanel(
            [FieldPanel("contact_title"), FieldPanel("contact_subtitle"), FieldPanel("contact_image")],
            heading="Contact section",
        ),
    ]

    seo_panels = seo_panels(disable_slug=False)

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Content"),
            ObjectList(seo_panels, heading="SEO"),
        ]
    )

    subpage_types = [
        "blog.BlogIndexPage",
    ]
    seo_content_type = SeoType.WEBSITE

    def get_admin_display_title(self) -> str:
        return "Home Page"

    def seo_image(self) -> str:
        """
        Gets the primary Open Graph image of this page.
        """
        from base.models import SEOSetting

        if self.hero_image:
            return self.hero_image
        if self.og_image:
            return self.og_image
        seo_defaults = SEOSetting.objects.first()
        return seo_defaults.seo_image if seo_defaults else None

    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"
