from django.conf import settings
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

from orionframework.media.registry import MediaRegistry
from orionframework.utils.reflection import require

registry = MediaRegistry(getattr(settings, "ORION_MEDIA_REGISTRY", []))

Document = registry.get_model("document")
Image = registry.get_model("image")
OnlineDocument = registry.get_model("online-document")

PREVIEW_ENABLED = getattr(settings, "ORION_DOCUMENT_PREVIEW_ENABLED", True)

PREVIEW_WIDTH = getattr(settings, "ORION_DOCUMENT_PREVIEW_WIDTH", 768)
PREVIEW_HEIGHT = getattr(settings, "ORION_DOCUMENT_PREVIEW_HEIGHT", 1024)

CHECKSUM_CALCULATOR = require(
    getattr(settings, "ORION_MEDIA_CHECKSUM_CALCULATOR", "orionframework.media.checksum.calculate_sha256"))

CONTENT_TYPE_CALCULATOR = require(
    getattr(settings, "ORION_MEDIA_CONTENT_TYPE_CALCULATOR", "orionframework.media.content_type.calculate"))

if Image:
    @receiver(pre_delete, sender=Image)
    def on_delete_image(sender, instance, **kwargs):
        instance.delete_file(instance.file)

if Document:
    @receiver(pre_delete, sender=Document)
    def on_delete_document(sender, instance, **kwargs):
        instance.delete_file(instance.file)
