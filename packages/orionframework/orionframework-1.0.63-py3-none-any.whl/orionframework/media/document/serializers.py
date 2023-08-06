from orionframework.media.image.serializers import ImageSerializer
from orionframework.media.serializers import AbstractFileMediaSerializer
from orionframework.media.settings import Document


class DocumentSerializer(AbstractFileMediaSerializer):
    preview = ImageSerializer(read_only=True)

    class Meta:
        model = Document
        exclude = ["parent_type", "parent_id", "file"]
