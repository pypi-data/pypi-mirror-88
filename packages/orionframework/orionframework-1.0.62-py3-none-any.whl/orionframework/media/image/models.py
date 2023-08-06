from django.conf import settings
from django.db import models
from django.db.models.fields.files import ImageFieldFile

from orionframework.media.models import MEDIA_PATH_RESOLVER, AbstractFileMedia


class AbstractImage(AbstractFileMedia):
    """
    Model used to map an image uploaded/attached to another model in the system.

    @since: 06/17/2014 20:30:00

    @author: orionframework
    """

    type = "image"
    """
    The unique type of document among the various registered document types.
    """

    file = models.ImageField('The image itself', upload_to=MEDIA_PATH_RESOLVER, width_field="width",
                             height_field="height", max_length=500)
    """
    The image itself
    """

    thumbnails_filesize = models.IntegerField(null=True, blank=True)
    """
    The number of bytes for all the generated thumbnails.
    """

    width = models.FloatField(null=True, blank=True)
    """
    The width (in pixels) for the image
    """

    height = models.FloatField(null=True, blank=True)
    """
    The height (in pixels) for the image
    """

    class Meta:
        abstract = True

    def to_json(self, thumbnail_name=None, **kwargs):

        if thumbnail_name:

            from easy_thumbnails.templatetags import thumbnail

            url = thumbnail.thumbnail_url(self.file, thumbnail_name)

        else:
            url = self.file.url

        return {
            "id": self.id,
            "title": self.title,
            "url": url
        }

    @property
    def urls(self):

        urls = {
            "original": self.url
        }

        from easy_thumbnails.templatetags import thumbnail
        aliases = getattr(settings, "THUMBNAIL_ALIASES", {})

        for value in aliases.values():

            for name in value.keys():
                url = thumbnail.thumbnail_url(self.file, name)

                urls[name] = url

        return urls

    def delete_file(self, _file):

        self.thumbnails_filesize = None

        if isinstance(_file, ImageFieldFile) and _file.name:

            self.storage.delete(_file.name)

        elif isinstance(_file, str):

            self.storage.delete(_file)

        try:
            from easy_thumbnails.files import get_thumbnailer

            thumbnailer = get_thumbnailer(_file)
            thumbnailer.delete_thumbnails()

        except ImportError:
            pass

    def copy(self, **kwargs):

        copy = super(AbstractImage, self).copy(**kwargs)

        aliases = getattr(settings, "THUMBNAIL_ALIASES", {})

        for value in aliases.values():

            for name in value.keys():
                copy.to_json(thumbnail_name=name)

        return copy

    def resolve_path(self, filename, resolver):

        if hasattr(self, "preview_source") and self.preview_source:
            return resolver(self.preview_source, "preview/" + filename, allow_override=False)

        return super(AbstractImage, self).resolve_path(filename, resolver)
