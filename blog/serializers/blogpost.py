from django.template.defaultfilters import truncatewords_html
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from base.serializers import ImageSerializer


class BlogPostPageSerializer(serializers.Serializer):
    # Page fields
    title = serializers.CharField()
    slug = serializers.CharField()
    # BlogPostPage fields
    subtitle = serializers.SerializerMethodField()
    image = ImageSerializer(rendition="width-1920|format-webp|webpquality-70")
    image_thumbnail = SerializerMethodField()
    body = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    # SEO fields
    seo_title = serializers.CharField()
    seo_description = serializers.CharField()
    seo_image = ImageSerializer(rendition="width-480|format-webp|webpquality-70")
    seo_author = serializers.CharField()

    def get_image_thumbnail(self, obj) -> str:
        """
        Create a thumbnail rendition of the image using the ImageSerializer and the 'image' as source.
        """
        if obj.image:
            return ImageSerializer(obj.image, rendition="width-480|format-webp|webpquality-70").data
        return None

    def get_subtitle(self, obj) -> str:
        """
        Truncate the subtitle to 100 characters.
        """
        return truncatewords_html(obj.subtitle, 25)
