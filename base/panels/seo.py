from django import forms
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
)


def seo_panels(disable_slug=False) -> list:
    widget = forms.TextInput()
    if disable_slug:
        # Completely leave out the slug field so there are no validation errors upon saving page.
        return [
            MultiFieldPanel(
                [
                    FieldPanel("seo_title"),
                    FieldPanel("search_description"),
                    FieldPanel("og_image"),
                ],
                _("Search and Social Previews"),
            )
        ]
    return [
        MultiFieldPanel(
            [
                FieldPanel("slug", widget=widget),
                FieldPanel("seo_title"),
                FieldPanel("search_description"),
                FieldPanel("og_image"),
            ],
            _("Search and Social Previews"),
        )
    ]
