from orionframework.media.serializers import AbstractMediaSerializer
from orionframework.media.settings import OnlineDocument


class OnlineDocumentSerializer(AbstractMediaSerializer):
    class Meta:
        model = OnlineDocument
        exclude = ["parent_type", "parent_id"]
