from orionframework.media.serializers import AbstractFileMediaSerializer
from orionframework.media.settings import Image


class ImageSerializer(AbstractFileMediaSerializer):
    class Meta:
        model = Image
        exclude = ["parent_type", "parent_id", "file"]
