import simplejson
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser
from rest_framework.response import Response

from orionframework.media import utils
from orionframework.media.serializers import *
from orionframework.media.utils import is_image


class MediaServiceMixin(object):
    """
    shared functionality for services to create and destroy media objects
    """

    def import_media(self, record, origin_url, origin_id=None, category=None, **kwargs):

        file = utils.download(origin_url)

        return self.create_media(record, file=file, origin_url=origin_url, origin_id=origin_id, category=category,
                                 **kwargs)

    def create_media(self, record, file=None, category=None, **kwargs):
        """
        @param record: parent record that the media belongs to

        @param file: file that is being attached as a document/image

        @param category: multiple types of files can be uploaded to a record and
                         when this happens we need to pass in the file category
        """

        type = kwargs.pop("type", None)

        if not type and file:
            if is_image(file):
                type = "image"

        if not type:
            type = "document"

        service_class = registry.get_service(type)
        service = service_class(parent=record)

        media = service.create(category=category, file=file, **kwargs)

        return media

    def update_media(self, record, media_id, media_type, **kwargs):
        """
        Update media information such as name or description for the given
        media object within the given record.

        Note that updating media's file is not supported. This can only be done
        by deleting the existing file and adding a new media record instead.
        """

        service = record.media_service_from_type(media_type)

        media = service.filter(id=media_id).get()

        service.update(media, **kwargs)

    def destroy_media(self, record, media_id, media_type):

        service = record.media_service_from_type(media_type)

        service.delete(id__in=[media_id])


class MediaViewMixin(object):
    list_media_serializer_class = MediaSerializer
    create_media_response_serializer_class = MediaSerializer
    media_service_class = MediaServiceMixin
    """
    shared functionality for views to interact with media objects
    """

    @action(detail=True, url_path="media")
    def list_media(self, request, pk):

        return self.list_media_by_type(request, pk, None)

    @action(detail=True, url_path="media/(?P<media_type>[-\w]+)")
    def list_media_by_type(self, request, pk, media_type):
        """
        Retrieve all media documents attached to the underlying record.

        @param media_type: the type of media (image|document)
        """

        instance = self.get_object()

        media = instance.get_media(media_type)

        serializer = self.list_media_serializer_class(instance=media, many=True)

        return Response(serializer.data)

    @action(detail=True, methods=["delete"], url_path="media/destroy/(?P<media_id>[\d+]+)/(?P<media_type>[-\w]+)")
    def destroy_media(self, request, pk, media_id, media_type):
        """
        Destroys an existing media entry within the given object, permanently 
        deleting all of its metadata and attached files - including thumbnails 
        for images.
        
        @param media_id: the media's primary key
        
        @param media_type: the type of media (image|document)
        """

        instance = self.get_object()

        service = self.media_service_class()

        service.destroy_media(instance, media_id, media_type)

        return Response({})

    @action(detail=True, methods=["put"], url_path="media/create",
            parser_classes=(FormParser, MultiPartParser, FileUploadParser))
    def create_media(self, request, pk, *args, **kwargs):
        """
        Attach a new media content to the bounding record.
                    
        @param metadata: An array of objects (JSON), each object containing name
            of the document being uploaded. Note that while sending multiple files,
            both file and metadata should match size and order.
        """

        record = self.get_object()

        documents = self._create_media(record, request)

        serializer = self.create_media_response_serializer_class(instance=documents, many=True)

        return Response(serializer.data, status=201)

    def _get_files(self, request):

        files = []

        for key in request.FILES.keys():

            for file in request.FILES.getlist(key):
                files.append(file)

        return files

    def _create_media(self, record, request, **kwargs):

        service = self.media_service_class()

        metadata = simplejson.loads(request.data.get("metadata")) if "metadata" in request.data else None
        data = simplejson.loads(request.data.get("data")) if "data" in request.data else None

        documents = list()

        files = self._get_files(request)

        i = 0
        for file in files:

            params = {
                **kwargs
            }

            if metadata:
                params.update(metadata[i])

            documents.append(service.create_media(record, file=file, **params))

            i += 1

        if data:

            for item in data:
                serializer_class = registry.get_serializer(item.get("type"))
                serializer = serializer_class(data=item)
                serializer.is_valid(raise_exception=True)

                documents.append(service.create_media(record, **serializer.validated_data))

        return documents

    @action(detail=True, methods=["patch"], url_path="media/update/(?P<media_id>[\d+]+)/(?P<media_type>[-\w]+)")
    def update_media(self, request, pk, media_id, media_type, *args, **kwargs):
        """
        Update data for an existing media record. Notice that updating the
        file itself is not supported.
        """

        record = self.get_object()

        service = self.media_service_class()

        serializer_class = registry.get_serializer(media_type)

        serializer = serializer_class(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        params = {}
        params.update(kwargs)
        params.update(serializer.validated_data)

        service.update_media(record, media_id, media_type, **params)

        return Response(status=status.HTTP_200_OK)


class MediaCategorizedViewMixin(MediaViewMixin):
    @action(detail=True, methods=["put"], url_path="media/create/(?P<category>[^/.]+)",
            parser_classes=(FormParser, MultiPartParser, FileUploadParser))
    def create_media(self, request, pk, category, *args, **kwargs):
        """
        Attach a new media content to the bounding record under a given category.
        
        @param category: the media category used to indicate the type of asset being 
            attached to the record. 
                    
        @param metadata: An array of objects (JSON), each object containing name
            of the document being uploaded. Note that while sending multiple files,
            both file and metadata should match size and order.
        """

        metadata = simplejson.loads(request.data.get("metadata")) if request.data.has_key("metadata") else None

        instance = self.get_object()

        service = self.media_service_class()

        category = int(category)

        entries = list()

        i = 0

        for file in request.data.values():

            if not hasattr(file, "file"):
                continue

            params = {}

            if metadata:
                params["name"] = metadata[i].get("name", None)
                params["description"] = metadata[i].get("description", None)

            entries.append(service.create_media(instance, file=file, category=category, **params))

            i += 1

        serializer = self.create_media_response_serializer_class(entries, many=True)

        return Response(serializer.data, status=201)


class MediaModelMixin(object):
    """
    shared functionality for models that manage orion media objects. 
    """

    def media_service_from_type(self, media_type):
        """
        Look up for a media service based on its type
        
        @param media_type: the type of media service
        
        @return service for the given media type (either ServiceImage or ServiceDocument)
        """
        from orionframework.media.settings import registry

        service_class = registry.get_service(media_type)

        return service_class(parent=self)

    def get_media(self, media_type=None):
        return self.media_service_from_type(media_type).all() if media_type else self.media

    @property
    def media(self):
        """
        Encapsulate all media documents and images. If there are different categories
        of documents this method will need to be overriden.
        """
        result = []

        from orionframework.media.settings import registry

        for media_type in registry.storage.keys():

            for record in self.media_service_from_type(media_type).all():
                result.append(record)

        result.sort(key=lambda item: item.title)

        return result

    def copy(self, **kwargs):
        """
        Copies all underlying documents under new instances/paths in the remote server.
        :param kwargs:
        :return:
        """

        new_model = super(MediaModelMixin, self).copy(**kwargs)

        for document in self.media:
            document.copy(parent_id=new_model.id)

        return new_model
