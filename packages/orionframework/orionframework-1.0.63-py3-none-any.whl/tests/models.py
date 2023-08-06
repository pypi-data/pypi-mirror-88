from orionframework.media.document.models import AbstractDocument
from orionframework.media.image.models import AbstractImage
from orionframework.media.remote_document.models import AbstractOnlineDocument


class Image(AbstractImage):
    pass


class Document(AbstractDocument):
    pass


class OnlineDocument(AbstractOnlineDocument):
    pass
