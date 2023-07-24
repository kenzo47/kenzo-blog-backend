from django.db.models import SET_NULL, CharField, DateTimeField, ForeignKey, Model
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet


@register_snippet
class Category(Model):
    """
    Model/snippet for blog categories.
    """

    name = CharField(
        max_length=100,
        blank=False,
        null=True,
        unique=True,
        verbose_name="Category name",
        help_text="Choose a name for the category.",
    )
    image = ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        on_delete=SET_NULL,
        related_name="+",
        verbose_name="Category image",
        help_text="Choose an image for the category.",
    )
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("image"),
    ]

    def __str__(self) -> str:
        return self.name
