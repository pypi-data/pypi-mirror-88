from orionframework.media.services import ServiceMedia
from orionframework.media.settings import Image


class ServiceImage(ServiceMedia):
    """
    Service used to manage the lifecycle of the Image model.
    """

    model_class = Image
