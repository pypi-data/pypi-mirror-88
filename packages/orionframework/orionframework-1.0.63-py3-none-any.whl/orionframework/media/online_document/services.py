from orionframework.media.services import ServiceMedia
from orionframework.media.settings import OnlineDocument


class ServiceOnlineDocument(ServiceMedia):
    """
    Service used to manage the lifecycle of the Remote document model.
    """

    model_class = OnlineDocument
