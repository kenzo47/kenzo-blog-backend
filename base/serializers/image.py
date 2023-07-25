from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from wagtail.images import get_image_model


class ImageSerializer(serializers.ModelSerializer):
    def __init__(self, *args, rendition="original", **kwargs) -> None:
        super(ImageSerializer, self).__init__(*args, **kwargs)
        self.rendition = rendition

    file = SerializerMethodField()
    width = SerializerMethodField()
    height = SerializerMethodField()

    def get_file(self, obj) -> str:
        return obj.get_rendition(self.rendition).file.url

    def get_width(self, obj) -> int:
        return obj.get_rendition(self.rendition).width

    def get_height(self, obj) -> int:
        return obj.get_rendition(self.rendition).height

    class Meta:
        model = get_image_model()
        fields = ["title", "file", "width", "height"]