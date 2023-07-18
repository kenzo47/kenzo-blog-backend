from django.db.models import SET_NULL, ForeignKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.settings.models import BaseGenericSetting
from wagtail.contrib.settings.registry import register_setting


@register_setting
class SEOSetting(BaseGenericSetting, ClusterableModel):
    seo_image = ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=SET_NULL,
        related_name="+",
    )

    panels = list[FieldPanel](
        [
            FieldPanel("seo_image"),
        ]
    )

    class Meta:
        verbose_name = "SEO Settings"
