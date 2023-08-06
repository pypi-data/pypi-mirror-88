from django.db import models

from orionframework.media.models import AbstractMedia

GOOGLE_DOCUMENT = "google/document"
GOOGLE_SPREADSHEET = "google/spreadsheet"
GOOGLE_PRESENTATION = "google/presentation"


class AbstractOnlineDocument(AbstractMedia):
    """
    Model used to map an online document residing on a external server. Note that sometimes the document
    may translate to a service rather than a file.

    @since: 12/29/2020 1:30:00

    @author: orionframework
    """

    type = "online-document"
    """
    The unique type of document among the various registered document types.
    """

    origin_type = models.CharField(null=True, blank=True, max_length=255, db_index=True)
    """
    The type of origin for this document, (google doc, google spreadsheet, google presentation, dropbox, etc.).
    """

    class Meta:
        abstract = True

    @property
    def url(self):
        return self.origin_url

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.origin_type:
            self.origin_type = self.extract_origin_type(self.url)

        return super(AbstractOnlineDocument, self).save(force_insert=force_insert, force_update=force_update,
                                                        using=using,
                                                        update_fields=update_fields)

    def extract_origin_type(self, url):

        if not url:
            return None

        if "google.com" in url:
            if "document" in url:
                return GOOGLE_DOCUMENT
            if "spreadsheets" in url:
                return GOOGLE_SPREADSHEET
            if "presentation" in url:
                return GOOGLE_PRESENTATION
